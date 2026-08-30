from __future__ import annotations

import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, render_template_string, request, send_file, redirect, url_for

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
EXCEL_EXPORT_PATH = BASE_DIR / "planilla_financiera.xlsx"


def money(value: Any) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class FinanceManager:
    def __init__(self) -> None:
        self.products = pd.DataFrame(
            [
                {
                    "code": "LIM-001",
                    "name": "Detergente industrial 5L",
                    "category": "Detergentes",
                    "unit_price": 180.00,
                    "cost_price": 95.00,
                    "stock": 120,
                    "min_stock": 30,
                },
                {
                    "code": "LIM-002",
                    "name": "Desinfectante multiuso 4L",
                    "category": "Desinfectantes",
                    "unit_price": 150.00,
                    "cost_price": 75.00,
                    "stock": 90,
                    "min_stock": 25,
                },
                {
                    "code": "LIM-003",
                    "name": "Jabón líquido para pisos",
                    "category": "Limpieza de superficies",
                    "unit_price": 200.00,
                    "cost_price": 110.00,
                    "stock": 70,
                    "min_stock": 20,
                },
            ]
        )
        self.clients = pd.DataFrame(
            [
                {
                    "client_id": "CLI-001",
                    "name": "Supermercado Casa Feliz",
                    "segment": "Minorista",
                    "contact": "ventas@casafeliz.cl",
                    "credit_limit": 50000.00,
                    "debt": 0.00,
                },
                {
                    "client_id": "CLI-002",
                    "name": "Hotel Los Pinos",
                    "segment": "Hospitalidad",
                    "contact": "compras@lospinos.cl",
                    "credit_limit": 75000.00,
                    "debt": 0.00,
                },
            ]
        )
        self.sales = pd.DataFrame(
            columns=[
                "sale_id",
                "client_id",
                "product_code",
                "quantity",
                "unit_price",
                "unit_cost",
                "date",
                "payment_method",
                "total",
            ]
        )
        self.purchases = pd.DataFrame(
            columns=[
                "purchase_id",
                "supplier",
                "product_code",
                "quantity",
                "unit_cost",
                "date",
                "total",
            ]
        )
        self.expenses = pd.DataFrame(
            columns=["expense_id", "category", "description", "amount", "date"]
        )

    def add_product(self, payload: dict) -> str:
        code = payload["code"].strip()
        if code in self.products["code"].astype(str).tolist():
            raise ValueError("El código ya existe")
        row = {
            "code": code,
            "name": payload["name"].strip(),
            "category": payload["category"].strip(),
            "unit_price": float(payload["unit_price"]),
            "cost_price": float(payload["cost_price"]),
            "stock": int(payload["stock"]),
            "min_stock": int(payload["min_stock"]),
        }
        self.products = pd.concat([self.products, pd.DataFrame([row])], ignore_index=True)
        return f"Producto agregado: {row['name']}"

    def add_client(self, payload: dict) -> str:
        client_id = payload["client_id"].strip()
        if client_id in self.clients["client_id"].astype(str).tolist():
            raise ValueError("El cliente ya existe")
        row = {
            "client_id": client_id,
            "name": payload["name"].strip(),
            "segment": payload["segment"].strip(),
            "contact": payload["contact"].strip(),
            "credit_limit": float(payload["credit_limit"]),
            "debt": 0.0,
        }
        self.clients = pd.concat([self.clients, pd.DataFrame([row])], ignore_index=True)
        return f"Cliente agregado: {row['name']}"

    def add_purchase(self, payload: dict) -> str:
        product_code = payload["product_code"].strip()
        if product_code not in self.products["code"].astype(str).tolist():
            raise ValueError("Producto inexistente")
        quantity = int(payload["quantity"])
        unit_cost = float(payload["unit_cost"])
        product_index = self.products.index[self.products["code"].astype(str) == product_code][0]
        self.products.at[product_index, "stock"] = int(self.products.at[product_index, "stock"]) + quantity
        total = money(unit_cost) * quantity
        new_row = {
            "purchase_id": f"CMP-{len(self.purchases) + 1:04d}",
            "supplier": payload["supplier"].strip(),
            "product_code": product_code,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": float(total),
        }
        self.purchases = pd.concat([self.purchases, pd.DataFrame([new_row])], ignore_index=True)
        return "Compra registrada correctamente"

    def add_sale(self, payload: dict) -> str:
        client_id = payload["client_id"].strip()
        product_code = payload["product_code"].strip()
        quantity = int(payload["quantity"])
        payment_method = payload.get("payment_method", "contado").strip().lower()

        if client_id not in self.clients["client_id"].astype(str).tolist():
            raise ValueError("Cliente inexistente")
        if product_code not in self.products["code"].astype(str).tolist():
            raise ValueError("Producto inexistente")

        product_index = self.products.index[self.products["code"].astype(str) == product_code][0]
        available = int(self.products.at[product_index, "stock"])
        if quantity > available:
            raise ValueError(f"Stock insuficiente. Disponible: {available}")

        unit_price = float(payload["unit_price"]) if payload.get("unit_price") else float(self.products.at[product_index, "unit_price"])
        unit_cost = float(self.products.at[product_index, "cost_price"])
        total = money(unit_price) * quantity
        self.products.at[product_index, "stock"] = available - quantity

        new_row = {
            "sale_id": f"VENT-{len(self.sales) + 1:04d}",
            "client_id": client_id,
            "product_code": product_code,
            "quantity": quantity,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payment_method": payment_method,
            "total": float(total),
        }
        self.sales = pd.concat([self.sales, pd.DataFrame([new_row])], ignore_index=True)

        if payment_method == "credito":
            client_index = self.clients.index[self.clients["client_id"].astype(str) == client_id][0]
            self.clients.at[client_index, "debt"] = float(self.clients.at[client_index, "debt"]) + float(total)
            return "Venta registrada en crédito"
        return "Venta registrada en contado"

    def add_expense(self, payload: dict) -> str:
        row = {
            "expense_id": f"GTO-{len(self.expenses) + 1:04d}",
            "category": payload["category"].strip(),
            "description": payload["description"].strip(),
            "amount": float(payload["amount"]),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.expenses = pd.concat([self.expenses, pd.DataFrame([row])], ignore_index=True)
        return "Gasto registrado correctamente"

    def financial_summary(self) -> dict:
        sales_total = float(self.sales["total"].sum()) if not self.sales.empty else 0.0
        cogs_total = float((self.sales["unit_cost"] * self.sales["quantity"]).sum()) if not self.sales.empty else 0.0
        operating_expenses = float(self.expenses["amount"].sum()) if not self.expenses.empty else 0.0
        inventory_value = float((self.products["cost_price"] * self.products["stock"]).sum()) if not self.products.empty else 0.0
        debt_total = float(self.clients["debt"].sum()) if not self.clients.empty else 0.0
        gross_profit = sales_total - cogs_total
        net_profit = gross_profit - operating_expenses
        margin = (net_profit / sales_total * 100) if sales_total else 0.0

        return {
            "sales_total": sales_total,
            "cogs_total": cogs_total,
            "gross_profit": gross_profit,
            "operating_expenses": operating_expenses,
            "net_profit": net_profit,
            "inventory_value": inventory_value,
            "debt_total": debt_total,
            "margin": margin,
        }

    def export_excel(self, output_path: Path) -> Path:
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            summary = pd.DataFrame([self.financial_summary()])
            summary.to_excel(writer, sheet_name="Resumen", index=False)
            self.products.to_excel(writer, sheet_name="Productos", index=False)
            self.clients.to_excel(writer, sheet_name="Clientes", index=False)
            self.sales.to_excel(writer, sheet_name="Ventas", index=False)
            self.purchases.to_excel(writer, sheet_name="Compras", index=False)
            self.expenses.to_excel(writer, sheet_name="Gastos", index=False)
        return output_path


manager = FinanceManager()


HTML_TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Startup de limpieza al por mayor</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: #f4f6fb;
      color: #1f2937;
    }
    .container {
      max-width: 1300px;
      margin: 20px auto;
      padding: 20px;
    }
    h1, h2 {
      margin-bottom: 12px;
    }
    .topbar {
      background: linear-gradient(135deg, #0f172a, #1d4ed8);
      color: white;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 20px;
    }
    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }
    .card {
      background: white;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 2px 8px rgba(15,23,42,0.08);
    }
    .card .label {
      color: #64748b;
      font-size: 13px;
      margin-bottom: 8px;
    }
    .card .value {
      font-size: 28px;
      font-weight: bold;
      color: #111827;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 18px;
      margin-bottom: 20px;
    }
    .panel {
      background: white;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 2px 8px rgba(15,23,42,0.08);
    }
    form {
      display: grid;
      gap: 10px;
    }
    input, select, button {
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      font-size: 14px;
    }
    button {
      background: #2563eb;
      color: white;
      border: none;
      cursor: pointer;
      font-weight: bold;
    }
    button.secondary {
      background: #0f766e;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 10px;
    }
    th, td {
      padding: 10px 8px;
      border-bottom: 1px solid #e2e8f0;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #eff6ff;
      color: #1e3a8a;
    }
    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .alert {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
      padding: 10px 12px;
      border-radius: 8px;
      margin-bottom: 16px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="topbar">
      <h1>Sistema financiero - Startup de limpieza al por mayor</h1>
      <p>Gestión de inventario, ventas, compras, gastos y exportación de datos a Excel.</p>
    </div>

    {% if message %}
      <div class="alert">{{ message }}</div>
    {% endif %}

    <div class="cards">
      <div class="card"><div class="label">Ventas</div><div class="value">$ {{ '%.2f' % summary.sales_total }}</div></div>
      <div class="card"><div class="label">Utilidad Bruta</div><div class="value">$ {{ '%.2f' % summary.gross_profit }}</div></div>
      <div class="card"><div class="label">Utilidad Neta</div><div class="value">$ {{ '%.2f' % summary.net_profit }}</div></div>
      <div class="card"><div class="label">Margen</div><div class="value">{{ '%.2f' % summary.margin }}%</div></div>
      <div class="card"><div class="label">Inventario</div><div class="value">$ {{ '%.2f' % summary.inventory_value }}</div></div>
      <div class="card"><div class="label">Deuda</div><div class="value">$ {{ '%.2f' % summary.debt_total }}</div></div>
    </div>

    <div class="actions">
      <h2>Datos financieros</h2>
      <a href="/export_excel"><button class="secondary">Exportar planilla Excel</button></a>
    </div>

    <div class="grid">
      <div class="panel">
        <h2>Agregar producto</h2>
        <form method="post" action="/add_product">
          <input name="code" placeholder="Código" required>
          <input name="name" placeholder="Nombre" required>
          <input name="category" placeholder="Categoría" required>
          <input name="unit_price" type="number" step="0.01" placeholder="Precio unitario" required>
          <input name="cost_price" type="number" step="0.01" placeholder="Costo unitario" required>
          <input name="stock" type="number" min="0" placeholder="Stock inicial" required>
          <input name="min_stock" type="number" min="0" placeholder="Stock mínimo" required>
          <button type="submit">Guardar</button>
        </form>
      </div>

      <div class="panel">
        <h2>Agregar cliente</h2>
        <form method="post" action="/add_client">
          <input name="client_id" placeholder="ID cliente" required>
          <input name="name" placeholder="Nombre" required>
          <input name="segment" placeholder="Segmento" required>
          <input name="contact" placeholder="Contacto" required>
          <input name="credit_limit" type="number" step="0.01" placeholder="Límite de crédito" required>
          <button type="submit">Guardar</button>
        </form>
      </div>

      <div class="panel">
        <h2>Registrar compra</h2>
        <form method="post" action="/add_purchase">
          <input name="supplier" placeholder="Proveedor" required>
          <input name="product_code" placeholder="Código de producto" required>
          <input name="quantity" type="number" min="1" placeholder="Cantidad" required>
          <input name="unit_cost" type="number" step="0.01" placeholder="Costo unitario" required>
          <button type="submit">Registrar compra</button>
        </form>
      </div>

      <div class="panel">
        <h2>Registrar venta</h2>
        <form method="post" action="/add_sale">
          <input name="client_id" placeholder="ID cliente" required>
          <input name="product_code" placeholder="Código de producto" required>
          <input name="quantity" type="number" min="1" placeholder="Cantidad" required>
          <input name="unit_price" type="number" step="0.01" placeholder="Precio venta unitario" required>
          <select name="payment_method">
            <option value="contado">Contado</option>
            <option value="credito">Crédito</option>
          </select>
          <button type="submit">Registrar venta</button>
        </form>
      </div>

      <div class="panel">
        <h2>Registrar gasto</h2>
        <form method="post" action="/add_expense">
          <input name="category" placeholder="Categoría" required>
          <input name="description" placeholder="Descripción" required>
          <input name="amount" type="number" step="0.01" placeholder="Monto" required>
          <button type="submit">Guardar gasto</button>
        </form>
      </div>
    </div>

    <div class="panel">
      <h2>Productos</h2>
      {{ products_table | safe }}
    </div>

    <div class="panel">
      <h2>Clientes</h2>
      {{ clients_table | safe }}
    </div>

    <div class="panel">
      <h2>Ventas</h2>
      {{ sales_table | safe }}
    </div>

    <div class="panel">
      <h2>Compras</h2>
      {{ purchases_table | safe }}
    </div>

    <div class="panel">
      <h2>Gastos</h2>
      {{ expenses_table | safe }}
    </div>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    summary = manager.financial_summary()
    products_table = manager.products.to_html(index=False, classes="table") if not manager.products.empty else "<p>No hay productos.</p>"
    clients_table = manager.clients.to_html(index=False, classes="table") if not manager.clients.empty else "<p>No hay clientes.</p>"
    sales_table = manager.sales.to_html(index=False, classes="table") if not manager.sales.empty else "<p>No hay ventas.</p>"
    purchases_table = manager.purchases.to_html(index=False, classes="table") if not manager.purchases.empty else "<p>No hay compras.</p>"
    expenses_table = manager.expenses.to_html(index=False, classes="table") if not manager.expenses.empty else "<p>No hay gastos.</p>"
    return render_template_string(
        HTML_TEMPLATE,
        summary=summary,
        products_table=products_table,
        clients_table=clients_table,
        sales_table=sales_table,
        purchases_table=purchases_table,
        expenses_table=expenses_table,
        message=request.args.get("message"),
    )


@app.route("/add_product", methods=["POST"])
def add_product_route():
    try:
        message = manager.add_product(request.form)
    except Exception as exc:
        message = f"Error: {exc}"
    return redirect(url_for("index", message=message))


@app.route("/add_client", methods=["POST"])
def add_client_route():
    try:
        message = manager.add_client(request.form)
    except Exception as exc:
        message = f"Error: {exc}"
    return redirect(url_for("index", message=message))


@app.route("/add_purchase", methods=["POST"])
def add_purchase_route():
    try:
        message = manager.add_purchase(request.form)
    except Exception as exc:
        message = f"Error: {exc}"
    return redirect(url_for("index", message=message))


@app.route("/add_sale", methods=["POST"])
def add_sale_route():
    try:
        message = manager.add_sale(request.form)
    except Exception as exc:
        message = f"Error: {exc}"
    return redirect(url_for("index", message=message))


@app.route("/add_expense", methods=["POST"])
def add_expense_route():
    try:
        message = manager.add_expense(request.form)
    except Exception as exc:
        message = f"Error: {exc}"
    return redirect(url_for("index", message=message))


@app.route("/export_excel")
def export_excel():
    output_path = manager.export_excel(EXCEL_EXPORT_PATH)
    return send_file(output_path, as_attachment=True, download_name="planilla_financiera.xlsx")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
