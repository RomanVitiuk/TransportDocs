from httpx import get
from json.decoder import JSONDecodeError


class DocsService:
    def get_docs_info(self, invoice_id: str):
        try:
            # localhost ip
            # response = get(url=f"http://localhost:8002/document/{invoice_id}/")
            # docker ip
            response = get(url=f"http://172.17.0.1:8002/document/{invoice_id}/")
            return response.json()
        except JSONDecodeError:
            return {"response": f"Document with number {invoice_id} dosn`t exist!"}
