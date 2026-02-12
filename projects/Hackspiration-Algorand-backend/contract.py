from pyteal import *
from beaker import *

# Constants
STATUS_FORMING = Int(0)
STATUS_ACTIVE = Int(1)
STATUS_DISSOLVED = Int(2)

class SubSharePool(Application):
    # Global State
    subscription_name = ApplicationStateValue(stack_type=TealType.bytes)
    admin_address = ApplicationStateValue(stack_type=TealType.bytes)
    cost_per_cycle = ApplicationStateValue(stack_type=TealType.uint64)
    max_members = ApplicationStateValue(stack_type=TealType.uint64)
    current_members = ApplicationStateValue(stack_type=TealType.uint64)
    cycle_duration = ApplicationStateValue(stack_type=TealType.uint64)
    renewal_timestamp = ApplicationStateValue(stack_type=TealType.uint64)
    total_deposited = ApplicationStateValue(stack_type=TealType.uint64)
    status = ApplicationStateValue(stack_type=TealType.uint64)

    # Local State (per member)
    deposited_amount = AccountStateValue(stack_type=TealType.uint64, default=Int(0))
    is_active = AccountStateValue(stack_type=TealType.uint64, default=Int(0))

    @create
    def create(self, subscription_name: abi.String, admin_address: abi.Address, cost_per_cycle: abi.Uint64, max_members: abi.Uint64, cycle_duration: abi.Uint64):
        return Seq(
            self.subscription_name.set(subscription_name.get()),
            self.admin_address.set(admin_address.get()),
            self.cost_per_cycle.set(cost_per_cycle.get()),
            self.max_members.set(max_members.get()),
            self.current_members.set(Int(0)),
            self.cycle_duration.set(cycle_duration.get()),
            self.renewal_timestamp.set(Global.latest_timestamp() + cycle_duration.get()),
            self.total_deposited.set(Int(0)),
            self.status.set(STATUS_FORMING),
        )

    @opt_in
    def opt_in(self):
        return Seq(
            Assert(self.status != STATUS_DISSOLVED),
            Assert(self.current_members < self.max_members),
            self.is_active.set(Int(1)),
            self.current_members.increment(),
        )

    @external
    def deposit_share(self, payment: abi.PaymentTransaction):
        return Seq(
            Assert(self.status != STATUS_DISSOLVED),
            Assert(payment.get().receiver() == Global.current_application_address()),
            self.deposited_amount.set(self.deposited_amount + payment.get().amount()),
            self.total_deposited.set(self.total_deposited + payment.get().amount()),
        )

    @external
    def payout(self):
        return Seq(
            Assert(self.total_deposited == self.cost_per_cycle),
            InnerTxnBuilder.Execute({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: self.admin_address,
                TxnField.amount: self.total_deposited,
            }),
            self.status.set(STATUS_ACTIVE),
            self.renewal_timestamp.set(self.renewal_timestamp + self.cycle_duration),
            self.total_deposited.set(Int(0)),
        )

    @external
    def renew_cycle(self):
        return Seq(
            Assert(Global.latest_timestamp() >= self.renewal_timestamp),
            self.payout(), # Triggers payout logic
        )
    
    @external
    def dissolve_pool(self):
        return Seq(
            Assert(Txn.sender() == self.admin_address),
            self.status.set(STATUS_DISSOLVED),
            # Ideally refund all here, but iterating over accounts is hard in AVM 
            # Simplified: Users withdraw manually if dissolved
        )

    @external
    def withdraw(self):
        # Allow withdrawal if dissolved
        return Seq(
            Assert(self.status == STATUS_DISSOLVED),
            InnerTxnBuilder.Execute({
                TxnField.type_enum: TxnType.Payment,
                TxnField.receiver: Txn.sender(),
                TxnField.amount: self.deposited_amount,
            }),
            self.deposited_amount.set(Int(0))
        )

    @external
    def exit_next_cycle(self):
        return self.is_active.set(Int(0))

if __name__ == "__main__":
    import json
    app = SubSharePool()
    print(app.application_spec().to_json())
