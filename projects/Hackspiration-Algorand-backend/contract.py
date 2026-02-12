from pyteal import *
from beaker import *
import beaker 

# Constants
STATUS_FORMING = Int(0)
STATUS_ACTIVE = Int(1)
STATUS_DISSOLVED = Int(2)

class SubShareState:
    # Global State
    subscription_name = GlobalStateValue(stack_type=TealType.bytes)
    admin_address = GlobalStateValue(stack_type=TealType.bytes)
    cost_per_cycle = GlobalStateValue(stack_type=TealType.uint64)
    max_members = GlobalStateValue(stack_type=TealType.uint64)
    current_members = GlobalStateValue(stack_type=TealType.uint64)
    cycle_duration = GlobalStateValue(stack_type=TealType.uint64)
    renewal_timestamp = GlobalStateValue(stack_type=TealType.uint64)
    total_deposited = GlobalStateValue(stack_type=TealType.uint64)
    status = GlobalStateValue(stack_type=TealType.uint64)

    # Local State (per member)
    deposited_amount = LocalStateValue(stack_type=TealType.uint64, default=Int(0))
    is_active = LocalStateValue(stack_type=TealType.uint64, default=Int(0))

app = Application("SubSharePool", state=SubShareState())

@app.create
def create(subscription_name: abi.String, admin_address: abi.Address, cost_per_cycle: abi.Uint64, max_members: abi.Uint64, cycle_duration: abi.Uint64):
    return Seq(
        app.state.subscription_name.set(subscription_name.get()),
        app.state.admin_address.set(admin_address.get()),
        app.state.cost_per_cycle.set(cost_per_cycle.get()),
        app.state.max_members.set(max_members.get()),
        app.state.current_members.set(Int(0)),
        app.state.cycle_duration.set(cycle_duration.get()),
        app.state.renewal_timestamp.set(Global.latest_timestamp() + cycle_duration.get()),
        app.state.total_deposited.set(Int(0)),
        app.state.status.set(STATUS_FORMING),
    )

@app.opt_in
def opt_in():
    return Seq(
        Assert(app.state.status != STATUS_DISSOLVED),
        Assert(app.state.current_members < app.state.max_members),
        app.state.is_active.set(Int(1)),
        app.state.current_members.increment(),
    )

@app.external
def deposit_share(payment: abi.PaymentTransaction):
    return Seq(
        Assert(app.state.status != STATUS_DISSOLVED),
        Assert(payment.get().receiver() == Global.current_application_address()),
        app.state.deposited_amount.set(app.state.deposited_amount + payment.get().amount()),
        app.state.total_deposited.set(app.state.total_deposited + payment.get().amount()),
    )

@app.external
def payout():
    return Seq(
        Assert(app.state.total_deposited == app.state.cost_per_cycle),
        InnerTxnBuilder.Execute({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: app.state.admin_address,
            TxnField.amount: app.state.total_deposited,
        }),
        app.state.status.set(STATUS_ACTIVE),
        app.state.renewal_timestamp.set(app.state.renewal_timestamp + app.state.cycle_duration),
        app.state.total_deposited.set(Int(0)),
    )

@app.external
def renew_cycle():
    return Seq(
        Assert(Global.latest_timestamp() >= app.state.renewal_timestamp),
        # Reuse payout logic if possible manually or duplicate
        Assert(app.state.total_deposited == app.state.cost_per_cycle),
        InnerTxnBuilder.Execute({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: app.state.admin_address,
            TxnField.amount: app.state.total_deposited,
        }),
        app.state.status.set(STATUS_ACTIVE),
        app.state.renewal_timestamp.set(app.state.renewal_timestamp + app.state.cycle_duration),
        app.state.total_deposited.set(Int(0)),
    )

@app.external
def dissolve_pool():
    return Seq(
        Assert(Txn.sender() == app.state.admin_address),
        app.state.status.set(STATUS_DISSOLVED),
    )

@app.external
def withdraw():
    return Seq(
        Assert(app.state.status == STATUS_DISSOLVED),
        InnerTxnBuilder.Execute({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: Txn.sender(),
            TxnField.amount: app.state.deposited_amount,
        }),
        app.state.deposited_amount.set(Int(0))
    )

@app.external
def exit_next_cycle():
    return app.state.is_active.set(Int(0))

if __name__ == "__main__":
    import json
    # For beaker 1.0, app.build() generates artifacts
    spec = app.build()
    print(json.dumps(spec.dict(), indent=2)) # Adjust based on what build returns
