
@classmethod
def listar_todas(cls):
    """Lista todas as operações trazendo o nome do comandante em 1 única query (JOIN)."""

    sql = """
        SELECT o.*, a.nome AS comandante_nome
        FROM operacoes o
        INNER JOIN agentes a ON o.comandante_id = a.id
        ORDER BY o.nivel_sigilo DESC, o.id DESC
    """

    with DatabaseConnection() as db:
        db.cursor.execute(sql)
        rows = db.cursor.fetchall()

        return [
            cls(
                id=r['id'],
                titulo=r['titulo'],
                divisao=r['divisao'],
                nivel_sigilo=r['nivel_sigilo'],
                relatorio_campo=r['relatorio_campo'],
                comandante_id=r['comandante_id'],
                comandante_nome=r['comandante_nome']
            )
            for r in rows
        ]