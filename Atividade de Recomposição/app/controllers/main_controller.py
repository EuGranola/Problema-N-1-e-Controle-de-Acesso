from flask import (Blueprint, render_template, request, redirect, url_for, flash, g)

@main_bp.route('/operacoes/nova', methods=['POST'])
@login_required
def criar_operacao():

    # MISSÃO 2 - Controle Baseado em Papel (RBAC)
    if g.agente.papel not in ('Diretor', 'Comandante'):
        flash(
            "Acesso negado (RBAC): Apenas Diretores e Comandantes podem criar operações.",
            "erro"
        )
        return redirect(url_for('main.dashboard'))

    titulo = request.form.get('titulo', '').strip()
    divisao = request.form.get('divisao', '').strip()
    nivel_sigilo = request.form.get('nivel_sigilo', '1')
    relatorio_campo = request.form.get('relatorio_campo', '').strip()

    if not titulo or not divisao or not relatorio_campo:
        flash("Preencha todos os campos obrigatórios da operação.", "erro")
        return redirect(url_for('main.dashboard'))

    nova_op = Operacao(
        titulo=titulo,
        divisao=divisao,
        nivel_sigilo=int(nivel_sigilo),
        relatorio_campo=relatorio_campo,
        comandante_id=g.agente.id
    )

    nova_op.salvar()
    flash(f"Operação '{titulo}' registrada com sucesso!", "sucesso")
    return redirect(url_for('main.dashboard'))

@main_bp.route('/operacoes/<int:operacao_id>')
@login_required
def detalhes_operacao(operacao_id):

    operacao = Operacao.buscar_por_id(operacao_id)

    if not operacao:
        flash("Operação não encontrada nos arquivos da S.H.I.E.L.D.", "erro")
        return redirect(url_for('main.dashboard'))

    # MISSÃO 3 - Controle Baseado em Atributos (ABAC)
    eh_diretor = (g.agente.papel == 'Diretor')

    atributos_validos = (
        g.agente.divisao == operacao.divisao
        and g.agente.nivel_credencial >= operacao.nivel_sigilo
    )

    if not (eh_diretor or atributos_validos):
        flash(
            f"Acesso negado (ABAC): Exige Divisão '{operacao.divisao}' e Credencial Nível {operacao.nivel_sigilo}.",
            "erro"
        )
        return redirect(url_for('main.dashboard'))

    return render_template('main/detalhes.html', operacao=operacao)

@main_bp.route('/operacoes/<int:operacao_id>/excluir', methods=['POST'])
@login_required
def excluir_operacao(operacao_id):

    operacao = Operacao.buscar_por_id(operacao_id)

    if not operacao:
        flash("Operação não encontrada.", "erro")
        return redirect(url_for('main.dashboard'))

    # MISSÃO 4 - Controle Baseado em Relacionamento / Autoria (ReBAC)
    eh_diretor = (g.agente.papel == 'Diretor')
    eh_comandante_criador = (operacao.comandante_id == g.agente.id)

    if not (eh_diretor or eh_comandante_criador):
        flash(
            "Acesso negado (ReBAC): Apenas o Comandante criador da operação ou o Diretor podem excluí-la.",
            "erro"
        )
        return redirect(url_for('main.dashboard'))

    Operacao.excluir(operacao_id)
    flash(f"Operação '{operacao.titulo}' arquivada/removida com sucesso.", "sucesso")
    return redirect(url_for('main.dashboard'))