from collections import defaultdict
from odoo import api, SUPERUSER_ID, models
import io
import os

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    module_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = "data/Postnummerregister-utf8.txt"
    file_path = os.path.join(module_dir, relative_path)

    country_norway = env["res.country"].search([("code", "=", "NO")], limit=1)
    if not country_norway:
        print("Error: Norway not found in res.country.  Please ensure it exists.")
        return  # Stop processing if Norway is not found

    city_cache = {}  # Cache to avoid duplicate city creation

    try:
        with io.open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    post_code = parts[0]
                    city_name = parts[1]

                    # Create or retrieve res.city
                    if city_name not in city_cache:
                        city = env["res.city"].create({
                            "name": city_name,
                            "country_id": country_norway.id,
                        })
                        city_cache[city_name] = city
                    else:
                        city = city_cache[city_name]

                    # Create res.city.zip
                    env["res.city.zip"].create({
                        "name": post_code,
                        "city_id": city.id,
                        "country_id": country_norway.id,
                    })

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")
