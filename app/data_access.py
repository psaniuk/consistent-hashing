from mysql.connector.aio import connect


async def execute_query(
    query: str, parameters: tuple, db_config: dict[str, str]
) -> any:
    async with await connect(**db_config) as connection:
        async with await connection.cursor() as cursor:
            await cursor.execute(query, parameters)
            result = await cursor.fetchall()
            await connection.commit()
            return result
