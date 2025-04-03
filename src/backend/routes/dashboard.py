
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from src.backend.utils.assets import get_asset_path
from src.backend.utils.db import get_db_cursor
from src.backend.models.sale import Sale
from src.backend.models.page import Page
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import random
import os
import uuid

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template(
        "frontend/index.html",
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

@dashboard_bp.route("/admin")
def admin_dashboard():
    return render_template(
        "admin/dashboard.html",
        page_title="Admin Dashboard",
        page_icon="🛠️",
        get_asset_path=get_asset_path
    )

@dashboard_bp.route("/admin/sales", methods=["GET", "POST"])
def admin_sales():
    try:
        page = int(request.args.get("page", 1))
        per_page = 10
        offset = (page - 1) * per_page

        with get_db_cursor() as cursor:
            if request.method == "POST":
                date = request.form.get("date")
                total = request.form.get("total")
                refunds = request.form.get("refunds")

                cursor.execute(
                    "INSERT INTO sales (date, total, refunds) VALUES (?, ?, ?)",
                    (date, total, refunds)
                )

            cursor.execute("SELECT COUNT(*) FROM sales")
            total_sales = cursor.fetchone()[0]

            cursor.execute(
                "SELECT id, date, total, refunds FROM sales ORDER BY date DESC LIMIT ? OFFSET ?",
                (per_page, offset)
            )
            rows = cursor.fetchall()

        sales = [Sale.from_row(r) for r in rows]

        return render_template(
            "admin/sales/list.html",
            get_asset_path=get_asset_path,
            page_title="Sales",
            page_icon="📊",
            sales=sales,
            current_page=page,
            has_next=(offset + per_page < total_sales),
            has_prev=(page > 1)
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
        return render_template("admin/sales/list.html", sale=sale, get_asset_path=get_asset_path, page_title="Edit Sale", page_icon="✏️")

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
    return render_template("frontend/page.html", page=page, page_title=page.title, get_asset_path=get_asset_path)


@dashboard_bp.route("/admin/pages")
def admin_pages():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM pages ORDER BY created_at DESC")
        rows = cursor.fetchall()
        pages = [Page.from_row(r) for r in rows]
    return render_template("admin/pages/list.html", pages=pages, get_asset_path=get_asset_path, page_title="Pages", page_icon="📄")


@dashboard_bp.route("/admin/pages/new", methods=["GET", "POST"])
def admin_new_page():
    if request.method == "POST":
        slug = request.form.get("slug")
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now().isoformat()
        next_action = request.form.get("next_action", "list")

        with get_db_cursor() as cursor:
            cursor.execute("SELECT id FROM pages WHERE slug = ?", (slug,))
            existing = cursor.fetchone()
            if existing:
                # 👇 Show error inline (or flash, up to you)
                error = f"A page with the slug '{slug}' already exists."
                return render_template(
                    "admin/pages/form.html",
                    page={"slug": slug, "title": title, "content": content},
                    get_asset_path=get_asset_path,
                    page_title="New Page",
                    page_icon="➕",
                    error=error
                )

            cursor.execute("""
                INSERT INTO pages (slug, title, content, created_at)
                VALUES (?, ?, ?, ?)
            """, (slug, title, content, created_at))

        if next_action == "view":
            return redirect(url_for("dashboard.view_page", slug=slug))
        return redirect(url_for("dashboard.admin_pages"))

    return render_template("admin/pages/form.html", page=None, get_asset_path=get_asset_path, page_title="New Page", page_icon="➕")

@dashboard_bp.route("/admin/pages/edit/<int:page_id>", methods=["GET", "POST"])
def admin_edit_page(page_id):
    with get_db_cursor() as cursor:
        if request.method == "POST":
            slug = request.form.get("slug")
            title = request.form.get("title")
            content = request.form.get("content")
            next_action = request.form.get("next_action", "list")

            cursor.execute("""
                UPDATE pages SET slug = ?, title = ?, content = ?
                WHERE id = ?
            """, (slug, title, content, page_id))

            if next_action == "view":
                return redirect(url_for("dashboard.view_page", slug=slug))
            return redirect(url_for("dashboard.admin_pages"))

        cursor.execute("SELECT * FROM pages WHERE id = ?", (page_id,))
        row = cursor.fetchone()
        if not row:
            return "Page not found", 404

        page = Page.from_row(row)

    return render_template("admin/pages/form.html", page=page, get_asset_path=get_asset_path, page_title="Edit Page", page_icon="✏️")

@dashboard_bp.route("/admin/pages/delete/<int:page_id>")
def delete_page(page_id):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        return redirect("/admin/pages")
    except Exception as e:
        return f"Error: {e}", 500

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

@dashboard_bp.route("/admin/upload-image", methods=["POST"])
def upload_page_image():
    file = request.files.get("image")
    if not file:
        return jsonify({
            'success': 0,
            'message': 'No file selected. Please choose an image to upload.'
        }), 400

    _, ext = os.path.splitext(file.filename.lower())
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({
            'success': 0,
            'message': f'Unsupported file type: {ext}. Allowed types are: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}.'
        }), 400

    safe_name = secure_filename(file.filename)
    filename = f"{uuid.uuid4().hex}_{safe_name}"

    upload_dir = os.path.join(dashboard_bp.root_path, '..', '..', '..', 'assets', 'pages')
    os.makedirs(upload_dir, exist_ok=True)

    try:
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
    except Exception as e:
        return jsonify({
            'success': 0,
            'message': f"Something went wrong while saving the file: {str(e)}"
        }), 500

    file_url = f"/assets/pages/{filename}"
    return jsonify({'success': 1, 'message': 'ok', 'url': file_url})

