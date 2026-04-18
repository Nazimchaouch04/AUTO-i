# TEST_2_EXISTING_BACKEND_TESTS.md - Exécution Tests Backend Existants

## Liste des Tests Existants (20+ fichiers)
```
test_ai_assistant.py
test_ai_simple.py
test_all_endpoints.py
test_config.py
test_db_connection.py
test_db_signals.py
test_gunicorn_performance.py
test_marketplace_complete.py
test_marketplace_models.py
test_models_fixed.py
test_models_simple.py
test_nlp_standalone_fixed.py
test_nlp_standalone.py
test_nlp_working.py
test_performance_prod.py
test_postgres_config.py
test_security_suite.py
test_simple_ai.py
autointel/tests.py
```

## Prochaine Commande (à exécuter)
```
cd backend
python manage.py test  # Django test runner
# OU
pytest apps/ -v --cov
```

## Objectif
- Couvrir API endpoints, modèles, DB, performance, sécurité.
- Générer rapport coverage HTML.

**À exécuter manuellement ou via nouveau script test_all_backend.bat**

**Statut: Tests existants identifiés et prêts !** 📋
