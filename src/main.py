import psycopg2
from groq import Groq
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
conn = psycopg2.connect("dbname = ecommerce_sales user=postgres password=lucifer54@")
cursor = conn.cursor()


client = Groq(
    api_key='API_KEY',
)

prompt_userQuery = """You are an expert SQL developer.

Your task is to convert natural language questions into SQL queries.

Database:
ecommerce_sales

Schema:
{
CATEGORIES: [category_id, category_name]
REGIONS: [region_id, region_name]
PRODUCTS: [product_id, product_name, category_id]
SALES: [sales_id,p_id,r_id,order_date,quantity,sales,profit]
}

Rules:
- Generate only SQL queries.
- Do not explain the query.
- If data is given in plural, make it singular. For example: Printers -> Printer
- Use only tables and columns provided in the schema.
- Use PostgreSQL syntax.
- Always use proper JOIN conditions.
- Use table aliases for readability.
- If the question cannot be answered using the schema, say "Cannot answer with given schema".

User Question:
"""


def ask_prompt(userQuery = "",prompt = prompt_userQuery):
    prompt += userQuery
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content


def performQuery(query):
    df = pd.read_sql(query, conn)
    return df

def formatResponse(user_query,sql_response):
    prompt_format = f"""The below is the result for this query: {user_query}. Please give a good and formatted answer which can be presented.- Do not explain the query.
 Result: """ + str(sql_response)
    format_response = ask_prompt(prompt = prompt_format)
    return format_response

def obtainStructure():
    query = """ SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';"""

    cursor.execute(query)
    tables = cursor.fetchall()
    table_hash = {table[0]: [] for table in tables}
    for table in tables:
        table_name = str(table[0])

        query = """SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s"""
        cursor.execute(query,(table_name,))
        data = cursor.fetchall()
        for col in data:
            table_hash[table_name].append(col[0])
    return table_hash





