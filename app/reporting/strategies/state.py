from datetime import date as date_type
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories.product import ProductRepository
from app.repositories.transaction import TransactionRepository
from .base import ReportStrategy


class StateStrategy(ReportStrategy):
    def generate(self, db: Session, target_date: date_type) -> Dict[str, Any]:
        product_repo = ProductRepository(db)
        trans_repo = TransactionRepository(db)

        products = product_repo.get_all()
        future_transactions = trans_repo.get_by_date(target_date)

        tx_map = {}
        for tx in future_transactions:
            tx_map.setdefault(tx.product_id, []).append(tx)

        product_details = []
        total_inventory_value = 0
        total_inventory_quantity = 0

        # 3. Основний цикл розрахунку для кожного продукту
        for p in products:
            # Початкова точка — поточна кількість
            qty_at_date = p.quantity

            # Якщо для цього продукту були транзакції після вказаної дати — "відкручуємо" їх
            if p.id in tx_map:
                for tx in tx_map[p.id]:
                    if tx.type == "ARRIVAL":
                        qty_at_date -= tx.quantity  # Віднімаємо прихід
                    elif tx.type in ["SHIPMENT", "WRITE_OFF"]:
                        qty_at_date += tx.quantity  # Повертаємо витрату

            # Розрахунок вартості на ту дату (qty * поточна ціна)
            value_at_date = qty_at_date * p.price

            # Додаємо дані по конкретному продукту
            product_details.append({
                "id": p.id,
                "name": p.name,
                "quantity": qty_at_date,
                "price": p.price,
                "value": value_at_date
            })

            # Оновлюємо загальні підсумки (Total)
            total_inventory_value += value_at_date
            total_inventory_quantity += qty_at_date

        # 4. Формуємо фінальний результат
        return {
            "report_type": f"Inventory State at {target_date}",
            "date": target_date,
            "total_value": round(total_inventory_value, 2),
            "total_quantity": total_inventory_quantity,
            "details": product_details
        }