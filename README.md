# Calisxtreme — atualizacoes oficiais pelo GitHub

Repositorio publico de **distribuicao do aplicativo**, nao de chaves privadas nem de backups. O aplicativo consulta o arquivo [update.json](update.json) e baixa APKs apenas apos autorizacao do usuario.

## Estado atual

- App instalado e testado: Calisxtreme 2.0 Beta 9.1, pacote `com.calisxtreme.app`, `versionCode 14`.
- O manifesto continua **desativado** (`enabled: false`) ate a primeira release oficial validada.
- Proxima versao preparada: **2.0.1**, `versionCode 15`.
- O Firebase usado no app e `calisxtreme-76510`. As regras Firestore sao gerenciadas separadamente e nao mudam ao publicar o APK.

## Publicar a atualizacao 2.0.1

1. No projeto Android Studio 2.0.1, execute `GERAR_APK_ASSINADO.cmd` em seu computador. Assine com o **certificado original**. Nunca envie a chave privada para o GitHub.
2. Confira que o arquivo e `Calisxtreme-2.0.1-assinado.apk` e teste a instalacao por cima da Beta 9.1 (preferencialmente com backup).
3. Execute `PUBLICAR_ATUALIZACAO_GITHUB.cmd` no projeto para validar pacote, versao e certificado; ele nao publica nada sem uma confirmacao explicita. Se o GitHub CLI nao estiver instalado, o script abre a pagina para publicacao manual.
4. Para publicar manualmente, abra [Nova release](https://github.com/SrDanvers/calisxtreme-atualizacoes/releases/new), crie a **tag `v2.0.1`**, titulo `Calisxtreme 2.0.1`, inclua exatamente **um APK oficial assinado** e a linha `Codigo: 15` na descricao. Use uma release normal, nao pre-release, apenas apos concluir os testes.
5. Quando a release for publicada, o workflow [.github/workflows/calisxtreme-atualizacoes.yml](.github/workflows/calisxtreme-atualizacoes.yml) checa assinatura, SHA-256, pacote, codigo de versao e nome de versao. Se tudo passar, atualiza automaticamente `update.json`.
6. Confirme o resultado em [Actions](https://github.com/SrDanvers/calisxtreme-atualizacoes/actions). No celular ainda com Beta 9.1, toque em **Perfil > Verificar atualizacoes**.

## Protecoes

- Pacote obrigatorio: `com.calisxtreme.app`.
- Certificado SHA-256 esperado: `cab25fb0ab0a691371281cf9dc00b0e258a9336794f4ac797b08a33de7510000`.
- Toda release oficial deve ter tag `vX.Y.Z`, nome de versao igual a tag sem `v`, e linha `Codigo: N` com versionCode do APK.
- Versoes marcadas como **pre-release** nao ativam atualizacoes e nao devem gerar erro no workflow.
- Nunca publique arquivos `.pk8`, `.pem`, `.jks`, a chave de assinatura em ZIP, segredos administrativos, senhas ou backups.
- O Android exige confirmacao para instalar; o aplicativo nao instala silenciosamente.
- Atualizacoes exigem internet; GPS, historico e metas locais continuam disponiveis offline.
- Teste login, Firestore, perfil oficial, GPS, exclusao de conta e preservacao de dados antes de distribuir a usuarios.
