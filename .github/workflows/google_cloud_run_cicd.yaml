name: Deploy to Cloud Run from Source

on:
  push:
    branches:
      - $default-branch

env:
  PROJECT_ID: baldrick # TODO: update Google Cloud project id
  SERVICE: baldrick # TODO: update Cloud Run service name
  REGION: us-central1 # TODO: update Cloud Run service region

jobs:
  deploy:
    # Add 'id-token' with the intended permissions for workload identity federation
    permissions:
      contents: 'read'
      id-token: 'write'

    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Google Auth
        id: auth
        uses: 'google-github-actions/auth@v0'
        with:
          workload_identity_provider: '${{ secrets.WIF_PROVIDER }}' # e.g. - projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
          service_account: '${{ secrets.WIF_SERVICE_ACCOUNT }}' # e.g. - my-service-account@my-project.iam.gserviceaccount.com

      # NOTE: Alternative option - authentication via credentials json
      # - name: Google Auth
      #   id: auth
      #   uses: 'google-github-actions/auth@v0'
      #   with:
      #     credentials_json: '${{ secrets.GCP_CREDENTIALS }}'

      - name: Deploy to Cloud Run
        id: deploy
        uses: google-github-actions/deploy-cloudrun@v0
        with:
          service: ${{ env.SERVICE }}
          region: ${{ env.REGION }}
          # NOTE: If required, update to the appropriate source folder
          source: ./

      # If required, use the Cloud Run url output in later steps
      - name: Show Output
        run: echo ${{ steps.deploy.outputs.url }}