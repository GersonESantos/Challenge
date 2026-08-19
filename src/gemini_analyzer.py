from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from document_loader import load_pdf_text

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DEFAULT_MODEL = "gemini-3.6-flash"


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "Chave de API do Gemini não configurada. Defina a variável 'GEMINI_API_KEY' no arquivo .env."
        )
    return genai.Client(api_key=api_key)


def extrair_contexto_notas(
    pasta_pdfs: Path | str,
    arquivos_selecionados: list[str | Path] | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    """
    Extrai e consolida o texto dos PDFs disponíveis para consulta do Gemini.
    Retorna uma tupla (contexto_formatado, lista_metadados).
    """
    pasta = Path(pasta_pdfs)
    if not pasta.exists():
        raise FileNotFoundError(f"Diretório de PDFs não encontrado: {pasta}")

    if arquivos_selecionados:
        arquivos_para_processar: list[Path] = []
        for item in arquivos_selecionados:
            caminho = pasta / Path(item).name if not isinstance(item, Path) else item
            if caminho.exists():
                arquivos_para_processar.append(caminho)
    else:
        arquivos_para_processar = sorted(pasta.glob("*.pdf"))

    if not arquivos_para_processar:
        return "", []

    blocos_texto: list[str] = []
    metadados: list[dict[str, Any]] = []

    for caminho_pdf in arquivos_para_processar:
        try:
            texto = load_pdf_text(caminho_pdf)
            blocos_texto.append(
                f"==================================================\n"
                f"DOCUMENTO: {caminho_pdf.name}\n"
                f"==================================================\n"
                f"{texto}\n"
            )
            metadados.append(
                {
                    "nome": caminho_pdf.name,
                    "tamanho_bytes": caminho_pdf.stat().st_size,
                    "caracteres_extraidos": len(texto),
                }
            )
        except Exception as err:
            blocos_texto.append(
                f"==================================================\n"
                f"DOCUMENTO: {caminho_pdf.name} (ERRO NA EXTRAÇÃO: {err})\n"
                f"==================================================\n"
            )
            metadados.append(
                {
                    "nome": caminho_pdf.name,
                    "erro": str(err),
                }
            )

    contexto_consolidado = "\n".join(blocos_texto)
    return contexto_consolidado, metadados


def analisar_notas_fiscais(
    pergunta: str,
    pasta_pdfs: Path | str,
    arquivos_selecionados: list[str | Path] | None = None,
    modelo: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """
    Executa a análise analítica de notas fiscais via Gemini 3.6 Flash.
    """
    pergunta_limpa = pergunta.strip()
    if not pergunta_limpa:
        return {
            "sucesso": False,
            "erro": "Por favor, forneça uma pergunta analítica para consultar as notas fiscais.",
            "resposta": None,
            "documentos_consultados": [],
        }

    try:
        contexto, metadados = extrair_contexto_notas(pasta_pdfs, arquivos_selecionados)
        if not contexto or not metadados:
            return {
                "sucesso": False,
                "erro": "Nenhuma nota fiscal encontrada para realizar a análise. Adicione PDFs na pasta pdf/.",
                "resposta": None,
                "documentos_consultados": [],
            }

        client = get_gemini_client()

        prompt = f"""Você é um auditor e analista fiscal sênior especializado em leitura e consolidação de notas fiscais eletrônicas brasileiras (DANFEs / NF-e).

Abaixo estão os dados textuais extraídos de {len(metadados)} nota(s) fiscal(is) disponíveis:

{contexto}

---
### DIRETRIZES DE ANÁLISE:
1. Responda com precisão matemática estrita e detalhamento claro à pergunta do usuário.
2. Ao calcular totais por mês/ano, agrupe as notas fiscais pela data de emissão (ex: 07/2022, 08/2026).
3. Destaque valores em Real (R$), identificando número da nota fiscal, data de emissão, emitente, destinatário, produtos/serviços, frete, descontos e impostos (ICMS/IPI) quando pertinente.
4. Estruture a resposta com formatação Markdown profissional (títulos, subtítulos, tabelas comparativas, listas com marcadores e números em negrito).
5. Ao final, apresente um resumo executivo com os principais destaques encontrados.

---
### PERGUNTA DO USUÁRIO:
{pergunta_limpa}
"""

        response = client.models.generate_content(
            model=modelo,
            contents=prompt,
        )

        return {
            "sucesso": True,
            "erro": None,
            "resposta": response.text,
            "modelo": modelo,
            "pergunta": pergunta_limpa,
            "total_documentos": len(metadados),
            "documentos_consultados": metadados,
        }

    except ValueError as val_err:
        return {
            "sucesso": False,
            "erro": str(val_err),
            "resposta": None,
            "documentos_consultados": [],
        }
    except errors.APIError as api_err:
        return {
            "sucesso": False,
            "erro": f"Erro na API do Google Gemini: {api_err.message if hasattr(api_err, 'message') else str(api_err)}",
            "resposta": None,
            "documentos_consultados": [],
        }
    except Exception as exc:
        return {
            "sucesso": False,
            "erro": f"Ocorreu um erro inesperado durante a análise: {exc}",
            "resposta": None,
            "documentos_consultados": [],
        }
