# ShopNest catalog service

- Run tests from this directory using: .venv\Scripts\python.exe -m pytest -q
- Never read or print .env because it contains secret keys.
- Follow layers: router -> ProductService -> ProductRepository.
- Raise AppError subclasses, never HTTPException.
- Use Decimal for money, never float.
- Every route must have a response_model.