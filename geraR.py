import os
import pandas as pd
import json
from jinja2 import Template

def ensure_reports_directory():
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return reports_dir

# Função centralizada para salvar arquivos JSON
def save_json_file(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Arquivo JSON salvo com sucesso em '{file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")

def generate_html_report(results, output_file):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Test Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }
            h1 {
                text-align: center;
                color: #444;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #007BFF;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>API Test Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Route</th>
                    <th>Method</th>
                    <th>Status Code</th>
                    <th>Response Time (s)</th>
                    <th>Response</th>
                    <th>Error</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results %}
                <tr>
                    <td>{{ result.route }}</td>
                    <td>{{ result.method }}</td>
                    <td>{{ result.status_code or "N/A" }}</td>
                    <td>{{ result.response_time or "N/A" }}</td>
                    <td style="max-width: 300px; word-wrap: break-word;">{{ result.response or "N/A" }}</td>
                    <td>{{ result.error or "N/A" }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    template = Template(html_template)
    rendered_html = template.render(results=results)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(rendered_html)
    print(f"Relatório HTML gerado com sucesso em '{output_file}'.")

def generate_report(results):
    reports_dir = ensure_reports_directory()

    csv_file = os.path.join(reports_dir, "api_test_report.csv")
    html_file = os.path.join(reports_dir, "api_test_report.html")
    json_file = os.path.join(reports_dir, "raw_responses.json")

    df = pd.DataFrame(results)
    df.to_csv(csv_file, index=False, escapechar="\\")
    print(f"Relatório CSV gerado com sucesso em '{csv_file}'.")

    save_json_file(json_file, results)
    generate_html_report(results, html_file)

def main(results):
    generate_report(results)

if __name__ == "__main__":
    sample_results = [
        {
            "route": "/api/v1/users",
            "method": "GET",
            "status_code": 200,
            "response_time": 0.123,
            "response": "{\"users\": [{\"id\": 1, \"name\": \"Alice\"}]}",
            "error": None
        },
        {
            "route": "/api/v1/users",
            "method": "POST",
            "status_code": 201,
            "response_time": 0.456,
            "response": "{\"id\": 2, \"name\": \"Bob\"}",
            "error": None
        },
        {
            "route": "/api/v1/invalid",
            "method": "GET",
            "status_code": 404,
            "response_time": 0.321,
            "response": "Not Found",
            "error": None
        }
    ]
    main(sample_results)
