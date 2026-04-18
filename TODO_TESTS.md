# TODO_TESTS.md - Plan de Tests SaaS AutoIntel

## Statut: ✅ Plan Approuvé - Exécution Progressive

### 1. [ ] Backend Tests Existants (Exécuter)
   - pytest sur tous test_*.py
   - Performance existants (test_performance_prod.py, etc.)

### 2. [ ] Setup Test Environments
   - Backend: pytest.ini + requirements-test.txt
   - Frontend: vitest.config.js + playwright

### 3. [ ] Backend Unit/Integration
   - API DRF complète: test_api_complete.py
   - Modèles SaaS: subscriptions, gamification: test_saas_models.py
   - ML Pricing: test_ml_engine.py

### 4. [ ] Backend Performance/Load
   - Locust: locustfile.py (500 users)
   - Apache Bench: test_load_ab.py

### 5. [ ] Backend Security
   - Bandit: test_security_bandit.py
   - Django security: test_security_django.py

### 6. [ ] Frontend Unit Tests
   - Vitest: tests/Header.test.jsx, tests/pages.test.jsx

### 7. [ ] Frontend E2E
   - Playwright: tests/e2e/login.spec.js, annonces.spec.js

### 8. [ ] SaaS-Specific
   - Subscriptions/Stripe mocks: test_subscriptions.py
   - Gamification/Alerts: test_gamification.py

### 9. [ ] CI/CD & Coverage
   - GitHub Actions: .github/workflows/tests.yml

### 10. [ ] Rapports Finaux
    - Coverage HTML, performance benchmarks

**Chaque test générera un fichier dédié explicatif !**  
**Prochaine étape: Backend existants → Nouveau test_api_complete.py**

Progression marquée ici après chaque étape.
