# Calisxtreme — atualizações automáticas (GitHub)

Repositório **público exclusivo de distribuição**. Não envie ZIP com chaves, keystores, credenciais, backups ou `google-services.json`.

Arquivos necessários: `update.json`, `.github/workflows/calisxtreme-atualizacoes.yml` e `scripts/atualizar_manifesto.py`.

O manifesto inicia com `enabled: false`. Uma release definitiva publicada com um APK assinado ativa o manifesto automaticamente, após validações do GitHub Actions.

O APK publicado precisa utilizar o pacote `com.calisxtreme.app` e o certificado original. O aplicativo solicita confirmação do usuário antes de instalar a atualização, nunca instala silenciosamente.
