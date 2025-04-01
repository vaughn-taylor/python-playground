
from flask import Blueprint, render_template, jsonify, request, redirect
from src.backend.utils.assets import get_asset_path
from src.backend.utils.db import get_db_cursor
from src.backend.models.sale import Sale
from src.backend.models.page import Page
from datetime import datetime, timedelta
import random

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        get_asset_path=get_asset_path,
        page_title="Data Dashboard",
        page_icon="📊"
    )

@dashboard_bp.route("/api/sales")
def api_sales():
    sales_data = []
    start = request.args.get("start")
    end = request.args.get("end")

    try:
        with get_db_cursor() as cursor:
            if start and end:
                query = "SELECT date, total, refunds FROM sales WHERE date BETWEEN ? AND ? ORDER BY date"
                cursor.execute(query, (start, end))
            else:
                query = "SELECT date, total, refunds FROM sales ORDER BY date"
                cursor.execute(query)

            rows = cursor.fetchall()
            for row in rows:
                sales_data.append({
                    "date": row["date"],
                    "total": row["total"],
                    "refunds": row["refunds"]
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(sales_data)

@dashboard_bp.route("/api/mock-sales")
def api_mock_sales():
    today = datetime.today()
    days = 14

    mock_data = []
    for i in range(days):
        date = (today - timedelta(days=days - i)).strftime("%Y-%m-%d")
        total = random.randint(100, 300)
        refunds = random.randint(5, 30)

        mock_data.append({
            "date": date,
            "total": total,
            "refunds": refunds
        })

    return jsonify(mock_data)

@dashboard_bp.route("/api/totals")
def api_totals():
    start = request.args.get("start")
    end = request.args.get("end")

    try:
        with get_db_cursor() as cursor:
            if start and end:
                cursor.execute("""
                    SELECT
                        SUM(total),
                        SUM(refunds),
                        AVG(total),
                        MIN(date),
                        MAX(date)
                    FROM sales
                    WHERE date BETWEEN ? AND ?
                """, (start, end))
            else:
                cursor.execute("""
                    SELECT
                        SUM(total),
                        SUM(refunds),
                        AVG(total),
                        MIN(date),
                        MAX(date)
                    FROM sales
                """)

            total, refunds, average, first_date, last_date = cursor.fetchone()

            result = {
                "total_sales": total or 0,
                "total_refunds": refunds or 0,
                "average_sales": round(average or 0, 2),
                "first_date": first_date,
                "last_date": last_date
            }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)

@dashboard_bp.route("/api/mock-totals")
def api_mock_totals():
    total_sales = random.randint(3000, 5000)
    total_refunds = random.randint(150, 400)
    avg_sales = round(total_sales / 14, 2)

    today = datetime.today()
    first_date = (today - timedelta(days=13)).strftime("%Y-%m-%d")
    last_date = today.strftime("%Y-%m-%d")

    return jsonify({
        "total_sales": total_sales,
        "total_refunds": total_refunds,
        "average_sales": avg_sales,
        "first_date": first_date,
        "last_date": last_date
    })

@dashboard_bp.route("/admin", methods=["GET", "POST"])
def admin_panel():
    try:
        with get_db_cursor() as cursor:
            if request.method == "POST":
                date = request.form.get("date")
                total = request.form.get("total")
                refunds = request.form.get("refunds")

                cursor.execute(
                    "INSERT INTO sales (date, total, refunds) VALUES (?, ?, ?)",
                    (date, total, refunds)
                )

            cursor.execute("SELECT id, date, total, refunds FROM sales ORDER BY date DESC LIMIT 25")
            rows = cursor.fetchall()

        sales = [Sale.from_row(r) for r in rows]

        return render_template(
            "admin.html",
            get_asset_path=get_asset_path,
            page_title="Admin",
            page_icon="🛠️",
            sales=sales
        )

    except Exception as e:
        return f"Error: {e}", 500

@dashboard_bp.route("/admin/edit/<int:sale_id>", methods=["GET", "POST"])
def edit_sale(sale_id):
    try:
        with get_db_cursor() as cursor:
            if request.method == "POST":
                date = request.form.get("date")
                total = request.form.get("total")
                refunds = request.form.get("refunds")

                cursor.execute(
                    "UPDATE sales SET date = ?, total = ?, refunds = ? WHERE id = ?",
                    (date, total, refunds, sale_id)
                )
                return redirect("/admin")

            cursor.execute("SELECT id, date, total, refunds FROM sales WHERE id = ?", (sale_id,))
            row = cursor.fetchone()

        if not row:
            return "Sale not found", 404

        sale = Sale.from_row(row)
        return render_template("edit_sale.html", sale=sale, get_asset_path=get_asset_path, page_title="Edit Sale", page_icon="✏️")

    except Exception as e:
        return f"Error: {e}", 500

@dashboard_bp.route("/admin/delete/<int:sale_id>")
def delete_sale(sale_id):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        return redirect("/admin")
    except Exception as e:
        return f"Error: {e}", 500


@dashboard_bp.route("/page/<slug>")
def view_page(slug):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM pages WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        if not row:
            return "Page not found", 404
        page = Page.from_row(row)
    return render_template("page.html", page=page, page_title=page.title, get_asset_path=get_asset_path)


@dashboard_bp.route("/admin/pages")
def admin_pages():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM pages ORDER BY created_at DESC")
        rows = cursor.fetchall()
        pages = [Page.from_row(r) for r in rows]
    return render_template("admin_pages.html", pages=pages, get_asset_path=get_asset_path, page_title="Pages", page_icon="📄")


@dashboard_bp.route("/admin/pages/new", methods=["GET", "POST"])
def admin_new_page():
    if request.method == "POST":
        slug = request.form.get("slug")
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now().isoformat()

        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO pages (slug, title, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (slug, title, content, created_at))

        return redirect("/admin/pages")

    return render_template("admin_page_form.html", page=None, get_asset_path=get_asset_path, page_title="New Page", page_icon="➕")


@dashboard_bp.route("/admin/pages/edit/<int:page_id>", methods=["GET", "POST"])
def admin_edit_page(page_id):
    with get_db_cursor() as cursor:
        if request.method == "POST":
            slug = request.form.get("slug")
            title = request.form.get("title")
            content = request.form.get("content")

            cursor.execute("""
                UPDATE pages SET slug = ?, title = ?, content = ?
                WHERE id = ?
            """, (slug, title, content, page_id))

            return redirect("/admin/pages")

        cursor.execute("SELECT * FROM pages WHERE id = ?", (page_id,))
        row = cursor.fetchone()
        if not row:
            return "Page not found", 404

        page = Page.from_row(row)

    return render_template("admin_page_form.html", page=page, get_asset_path=get_asset_path, page_title="Edit Page", page_icon="✏️")

