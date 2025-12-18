# Contributing to NODO x402 Protocol

We welcome contributions! This document provides guidelines for contributing to the project.

## How to Contribute

### 1. Report Issues

Found a bug or have a feature request?

- Check [existing issues](https://github.com/nodo-ai/nodo-x402-protocol/issues)
- If none exist, [create a new issue](https://github.com/nodo-ai/nodo-x402-protocol/issues/new)
- Provide as much detail as possible:
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment (OS, Python/Node version)
  - Error messages/logs

### 2. Submit Pull Requests

#### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/nodo-ai/nodo-x402-protocol
cd nodo-x402-protocol

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
ruff check .
black --check .
```

#### Create a Pull Request

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make your changes**
   - Write tests for new features
   - Update documentation
   - Follow code style

4. **Run tests**
   ```bash
   pytest
   ruff check .
   black .
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature"
   ```
   
   Use [conventional commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `test:` - Tests
   - `refactor:` - Code refactoring
   - `chore:` - Maintenance

6. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```
   Then create a pull request on GitHub.

### 3. Code Style

#### Python

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [Ruff](https://docs.astral.sh/ruff/) for linting
- Add type hints

```python
# Good
async def verify_payment(
    tx_signature: str,
    expected_amount: float
) -> Dict[str, Any]:
    """Verify USDC payment on Solana."""
    ...
```

#### TypeScript

- Follow [TypeScript guidelines](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- Use Prettier for formatting
- Use ESLint for linting

```typescript
// Good
async function verifyPayment(
  txSignature: string,
  expectedAmount: number
): Promise<VerificationResult> {
  // ...
}
```

### 4. Testing

All new features must include tests:

```python
# test_x402.py
async def test_payment_verification():
    """Test that valid payments are accepted."""
    client = SolanaPaymentClient()
    
    result = await client.verify_usdc_transfer(
        tx_signature="valid_signature",
        expected_amount=0.10
    )
    
    assert result["valid"] == True
```

Run tests:
```bash
pytest
pytest --cov  # With coverage
```

### 5. Documentation

Update documentation for any changes:

- Update `README.md` if changing public API
- Update `docs/` for detailed changes
- Add docstrings to new functions
- Update examples if needed

## Development Guidelines

### Middleware Changes

When modifying `src/middleware/x402.py`:

1. Test with multiple payment scenarios
2. Ensure backward compatibility
3. Update protocol version if needed
4. Document breaking changes

### SDK Changes

When modifying SDKs:

1. Keep Python and TypeScript in sync
2. Update both README files
3. Bump version in `setup.py` / `package.json`
4. Test with real Solana transactions

### Security

For security-related changes:

1. Don't commit secrets/keys
2. Add tests for edge cases
3. Document security implications
4. Consider reporting privately first

## Community

- **Discord**: [Join our server](https://discord.gg/nodo)
- **Email**: dev@nodo.ai
- **Twitter**: [@nodo_ai](https://twitter.com/nodo_ai)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

