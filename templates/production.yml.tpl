on: deployment

name: Production

jobs:
  deploy-production:
    if: github.event.deployment.ref == 'main' && github.event.deployment.environment == 'production'

    runs-on: ubuntu-latest
    container: python:$python_version-slim

    steps:
      - name: Checkout
        uses: actions/checkout@v2