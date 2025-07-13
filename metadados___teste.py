# [File: metadados.py]
import re
import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import logging


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class SugestorTags:
    def __init__(self):
        self.palavras_chave = {
            "Contrato": ["contrato", "cláusula", "vigência", "partes"],
            "Nota Fiscal": ["nota fiscal", "nfe", "danfe", "emitente", "destinatário"],
            "Certificado": ["certificado", "credenciamento", "homologação"],
            "Fatura": ["fatura", "vencimento", "valor total"],
            "Relatório": ["relatório", "conclusão", "análise"]
        }
        self.logger = logging.getLogger('SugestorTags')
        
    def extrair_texto(self, arquivo_path):
        """Extrai texto de diferentes tipos de arquivo"""
        _, ext = os.path.splitext(arquivo_path)
        texto = ""
        
        try:
            if ext.lower() in ['.pdf']:
                # Extrair texto de PDF
                doc = fitz.open(arquivo_path)
                for page in doc:
                    texto += page.get_text() + "\n"
                    
            elif ext.lower() in ['.png', '.jpg', '.jpeg']:
                # Extrair texto de imagem (OCR)
                imagem = Image.open(arquivo_path)
                texto = pytesseract.image_to_string(imagem, lang='por')
            
            elif ext.lower() in ['.docx', '.doc']:
                # Para documentos Word, precisaríamos de outra biblioteca
                # Mas vamos apenas usar o nome do arquivo por enquanto
                texto = os.path.basename(arquivo_path)
                
            else:
                # Para outros tipos, use apenas o nome do arquivo
                texto = os.path.basename(arquivo_path)
                
        except Exception as e:
            self.logger.error(f"Erro ao extrair texto de {arquivo_path}: {str(e)}")
        
        return texto.lower() if texto else ""
    
    def sugerir_tags(self, arquivo_path):
        """Sugere tags baseadas no conteúdo do arquivo"""
        texto = self.extrair_texto(arquivo_path)
        tags_sugeridas = []
        
        if not texto:
            return tags_sugeridas
        
        try:
            for tag, palavras in self.palavras_chave.items():
                for palavra in palavras:
                    if re.search(r'\b' + re.escape(palavra) + r'\b', texto):
                        tags_sugeridas.append(tag)
                        break  # Uma ocorrência basta para sugerir a tag
            
            # Sugerir baseado no nome do arquivo
            nome_arquivo = os.path.basename(arquivo_path).lower()
            if "contrat" in nome_arquivo:
                tags_sugeridas.append("Contrato")
            if "nf" in nome_arquivo or "nota" in nome_arquivo:
                tags_sugeridas.append("Nota Fiscal")
            if "fatur" in nome_arquivo:
                tags_sugeridas.append("Fatura")
                
        except Exception as e:
            self.logger.error(f"Erro ao sugerir tags para {arquivo_path}: {str(e)}")
        
        return list(set(tags_sugeridas))  # Remove duplicatas