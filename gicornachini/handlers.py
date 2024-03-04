from datetime import datetime

from aiohttp import web
from psycopg2.errors import ForeignKeyViolation

def is_transaction_invalid(valor, tipo, descricao):
    return (valor <= 0 \
            or type(valor) != int \
            or descricao is None \
            or len(descricao) == 0 or len(descricao) > 10 \
            or (tipo != "c" and tipo != "d"));

def transaction_format(db_response):
    evaluated_db_response = eval(db_response[0])
    status_code = evaluated_db_response[0]

    customer_response = evaluated_db_response[1] if len(evaluated_db_response) > 1 else None
    if customer_response:
        response_result = []
        splitted = customer_response.replace("{", "").replace("}", "").split(", ")
        for s in splitted:
            response_result.append(s.strip().split(' : '))
        return status_code, dict(response_result)
    return status_code, customer_response


async def transaction(request):
    customer_id = request.match_info['id']

    data = await request.json()
    valor = data["valor"]
    tipo = data["tipo"]
    descricao = data["descricao"]
    if is_transaction_invalid(valor, tipo, descricao):
        return web.json_response({}, status=400)

    db_pool = request.app['db_pool']
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"select transacao({customer_id},{valor},'{tipo}','{descricao}')")
                db_result = await cur.fetchone()
    except ForeignKeyViolation:
        return web.json_response({}, status=404)

    status_code, customer_response = transaction_format(db_result)
    if status_code == 0:
        return web.json_response(customer_response)
        
    return web.json_response({}, status=422)

def format_customer_credit_info_from_statement(statement_db_response):
    first_line = statement_db_response[0]
    return {
        "total": first_line[1],
        "data_extrato": datetime.now().isoformat(),
        "limite": first_line[0]
    }

def format_statement(statement_db_response_row):
    return {
      "valor": statement_db_response_row[5],
      "tipo": statement_db_response_row[4],
      "descricao": statement_db_response_row[6],
      "realizada_em": statement_db_response_row[7].isoformat()
    }

async def statement(request):
    customer_id = request.match_info['id']

    db_pool = request.app['db_pool']
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"select * from extrato({customer_id})")
            db_response = await cur.fetchall()

    if not db_response:
        return web.json_response({}, status=404)

    customer_credit_info = format_customer_credit_info_from_statement(db_response)
    last_statements = list(map(format_statement, db_response)) if db_response[0][2] else []

    return web.json_response({"saldo": customer_credit_info,
                              "ultimas_transacoes": last_statements}, status=200)
