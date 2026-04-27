#!/usr/bin/env python3
"""Manage jaffle_shop seed CSV data — add new records or update existing ones."""

import argparse
import csv
import random
import sys
from datetime import date, timedelta
from pathlib import Path

SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds"

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "William",
    "Linda", "Richard", "Barbara", "Joseph", "Susan", "Thomas", "Jessica",
    "Charles", "Sarah", "Christopher", "Karen", "Daniel", "Lisa", "Matthew",
    "Nancy", "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra",
    "Steven", "Ashley", "Andrew", "Dorothy", "Joshua", "Kimberly", "Kenneth",
    "Emily", "Kevin", "Donna", "Brian", "Michelle", "George", "Carol",
    "Timothy", "Amanda", "Ronald", "Melissa", "Edward", "Deborah", "Jason",
    "Stephanie",
]

LAST_INITIALS = [
    "A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.", "L.",
    "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.",
]

STATUSES = ["placed", "shipped", "completed", "return_pending", "returned"]
PAYMENT_METHODS = ["credit_card", "coupon", "bank_transfer", "gift_card"]


def read_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def next_id(rows: list[dict], field: str = "id") -> int:
    return max(int(r[field]) for r in rows) + 1 if rows else 1


def latest_date(rows: list[dict], field: str = "order_date") -> date:
    dates = [date.fromisoformat(r[field]) for r in rows if r.get(field)]
    return max(dates) if dates else date(2018, 1, 1)


def add_customers(n: int) -> list[dict]:
    rows = read_csv(SEEDS_DIR / "raw_customers.csv")
    start_id = next_id(rows)
    new = []
    for i in range(n):
        new.append({
            "id": str(start_id + i),
            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_INITIALS),
        })
    rows.extend(new)
    write_csv(SEEDS_DIR / "raw_customers.csv", rows, ["id", "first_name", "last_name"])
    return new


def add_orders(n: int, customer_ids: list[int] | None = None) -> list[dict]:
    customers = read_csv(SEEDS_DIR / "raw_customers.csv")
    orders = read_csv(SEEDS_DIR / "raw_orders.csv")

    if customer_ids is None:
        customer_ids = [int(c["id"]) for c in customers]

    start_id = next_id(orders)
    start_date = latest_date(orders) + timedelta(days=1)

    new = []
    for i in range(n):
        order_date = start_date + timedelta(days=random.randint(0, 30))
        new.append({
            "id": str(start_id + i),
            "user_id": str(random.choice(customer_ids)),
            "order_date": order_date.isoformat(),
            "status": random.choice(STATUSES),
        })
    # Sort by date for consistency
    new.sort(key=lambda r: r["order_date"])

    orders.extend(new)
    write_csv(SEEDS_DIR / "raw_orders.csv", orders, ["id", "user_id", "order_date", "status"])
    return new


def add_payments(orders: list[dict] | None = None) -> list[dict]:
    """Generate 1-3 payments per order. If orders is None, generates for all unpaid orders."""
    existing_payments = read_csv(SEEDS_DIR / "raw_payments.csv")
    all_orders = read_csv(SEEDS_DIR / "raw_orders.csv")

    paid_order_ids = {p["order_id"] for p in existing_payments}

    if orders is None:
        # Find orders without payments
        unpaid = [o for o in all_orders if o["id"] not in paid_order_ids]
        if not unpaid:
            print("All orders already have payments.")
            return []
        target_orders = unpaid
    else:
        target_orders = orders

    start_id = next_id(existing_payments)
    new = []
    for order in target_orders:
        order_id = order["id"]
        num_payments = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        total = random.randint(100, 5000)

        for j in range(num_payments):
            if j == num_payments - 1:
                amount = total  # Last payment gets the remainder
            else:
                amount = random.randint(0, total)
                total -= amount

            new.append({
                "id": str(start_id),
                "order_id": order_id,
                "payment_method": random.choice(PAYMENT_METHODS),
                "amount": str(amount),
            })
            start_id += 1

    existing_payments.extend(new)
    write_csv(
        SEEDS_DIR / "raw_payments.csv",
        existing_payments,
        ["id", "order_id", "payment_method", "amount"],
    )
    return new


def update_order_status(order_id: int, new_status: str) -> dict | None:
    if new_status not in STATUSES:
        print(f"Invalid status '{new_status}'. Must be one of: {', '.join(STATUSES)}")
        return None

    orders = read_csv(SEEDS_DIR / "raw_orders.csv")
    for row in orders:
        if row["id"] == str(order_id):
            old = row["status"]
            row["status"] = new_status
            write_csv(SEEDS_DIR / "raw_orders.csv", orders, ["id", "user_id", "order_date", "status"])
            print(f"Order {order_id}: {old} -> {new_status}")
            return row

    print(f"Order {order_id} not found.")
    return None


def update_customer(customer_id: int, first_name: str | None, last_name: str | None) -> dict | None:
    customers = read_csv(SEEDS_DIR / "raw_customers.csv")
    for row in customers:
        if row["id"] == str(customer_id):
            if first_name:
                row["first_name"] = first_name
            if last_name:
                row["last_name"] = last_name
            write_csv(SEEDS_DIR / "raw_customers.csv", customers, ["id", "first_name", "last_name"])
            print(f"Customer {customer_id} updated: {row}")
            return row

    print(f"Customer {customer_id} not found.")
    return None


def cmd_add(args: argparse.Namespace) -> None:
    match args.entity:
        case "customers":
            new = add_customers(args.count)
            for c in new:
                print(f"  + Customer {c['id']}: {c['first_name']} {c['last_name']}")
            print(f"Added {len(new)} customer(s).")

        case "orders":
            customer_ids = None
            if args.customer_id:
                customer_ids = [args.customer_id]
            new_orders = add_orders(args.count, customer_ids)
            new_payments = add_payments(new_orders)
            for o in new_orders:
                print(f"  + Order {o['id']}: customer={o['user_id']} date={o['order_date']} status={o['status']}")
            print(f"Added {len(new_orders)} order(s) with {len(new_payments)} payment(s).")

        case "full":
            # Add customers, then orders for those customers, then payments
            new_customers = add_customers(args.count)
            new_customer_ids = [int(c["id"]) for c in new_customers]
            new_orders = add_orders(args.count * 2, new_customer_ids)
            new_payments = add_payments(new_orders)
            print(f"Added {len(new_customers)} customer(s), {len(new_orders)} order(s), {len(new_payments)} payment(s).")


def cmd_update(args: argparse.Namespace) -> None:
    match args.entity:
        case "order":
            update_order_status(args.id, args.status)

        case "customer":
            update_customer(args.id, args.first_name, args.last_name)


def cmd_status(args: argparse.Namespace) -> None:
    customers = read_csv(SEEDS_DIR / "raw_customers.csv")
    orders = read_csv(SEEDS_DIR / "raw_orders.csv")
    payments = read_csv(SEEDS_DIR / "raw_payments.csv")

    print(f"Customers: {len(customers)}")
    print(f"Orders:    {len(orders)}")
    print(f"Payments:  {len(payments)}")

    status_counts = {}
    for o in orders:
        status_counts[o["status"]] = status_counts.get(o["status"], 0) + 1
    print("\nOrder statuses:")
    for s in STATUSES:
        print(f"  {s}: {status_counts.get(s, 0)}")

    paid_order_ids = {p["order_id"] for p in payments}
    unpaid = [o for o in orders if o["id"] not in paid_order_ids]
    if unpaid:
        print(f"\nOrders without payments: {len(unpaid)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage jaffle_shop seed data")
    sub = parser.add_subparsers(dest="command", required=True)

    # --- add ---
    p_add = sub.add_parser("add", help="Add new records")
    p_add.add_argument("entity", choices=["customers", "orders", "full"],
                        help="What to add (full = customers + orders + payments)")
    p_add.add_argument("-n", "--count", type=int, default=5, help="Number to add (default: 5)")
    p_add.add_argument("--customer-id", type=int, help="For orders: assign to specific customer")
    p_add.add_argument("--seed", type=int, help="Random seed for reproducibility")
    p_add.set_defaults(func=cmd_add)

    # --- update ---
    p_upd = sub.add_parser("update", help="Update existing records")
    p_upd_sub = p_upd.add_subparsers(dest="entity", required=True)

    p_upd_order = p_upd_sub.add_parser("order", help="Update an order's status")
    p_upd_order.add_argument("id", type=int, help="Order ID")
    p_upd_order.add_argument("status", choices=STATUSES, help="New status")

    p_upd_cust = p_upd_sub.add_parser("customer", help="Update a customer's name")
    p_upd_cust.add_argument("id", type=int, help="Customer ID")
    p_upd_cust.add_argument("--first-name", help="New first name")
    p_upd_cust.add_argument("--last-name", help="New last name")
    p_upd.set_defaults(func=cmd_update)

    # --- status ---
    p_status = sub.add_parser("status", help="Show seed data summary")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if hasattr(args, "seed") and args.seed is not None:
        random.seed(args.seed)

    args.func(args)


if __name__ == "__main__":
    main()
