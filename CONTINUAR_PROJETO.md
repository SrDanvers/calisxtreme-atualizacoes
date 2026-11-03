# Calisxtreme — ponto de retomada

Atualizado em: 03/11/2026.

## Estado confirmado
- Versao mais recente publicada e ativada no GitHub: **2.0.2** (`versionCode 16`), pacote `com.calisxtreme.app`.
- Release: https://github.com/SrDanvers/calisxtreme-atualizacoes/releases/tag/v2.0.2
- Manifesto de atualizacao: https://github.com/SrDanvers/calisxtreme-atualizacoes/blob/main/update.json — `enabled: true`, `latestVersionCode: 16`.
- APK SHA-256 publico: `b3de58ff195da076c3c11311286af94dc56b12304ade081c6b74bcf36df64a25`.
- GitHub Actions validou e publicou o manifesto com sucesso. Suporta instalacao sobre versao anterior com confirmacao do Android.
- Usuario testou o APK 2.0.2 no Android e aprovou o novo layout.
- Versao anterior 2.0.1 foi a primeira atualizacao efetivamente instalada pelo fluxo do aplicativo.
- Firebase projeto `calisxtreme-76510`; login e edicao do perfil oficial foram corrigidos anteriormente.

## Recursos e estilo
- Interface preta e amarela, **sem emojis**; visual moderno, botoes e icones discretos.
- Perfil do usuario com banner, foto, nome, bio, contadores e publicacoes na area principal.
- Menu de tres pontos com: Conquistas esportivas; Selos e verificacao; Atualizacoes; Conta e privacidade; Area do proprietario; Sair da conta; opcoes futuras. Versao 2.0.2 inclui tambem Sobre o criador e telas de seguranca.
- Sobre o criador: credito **Denny Ximenes**; preferencia por exibir o credito na tela Sobre, nao poluir o restante.
- GPS, historico e metas locais offline. Perfis, seguidores, autenticacao e publicacoes usam Firebase quando disponivel.
- Perfil oficial `@calisxtreme` com foto/banner editaveis somente pelo proprietario autenticado. Seguir conta oficial deve permanecer fixo. Selos de verificacao protegidos contra edicao pelo cliente.

## Ponto de partida da proxima sessao
1. Continuar a partir da versao **2.0.3**, `versionCode 17` (nao reutilizar codigo 16).
2. Preservar o applicationId, certificado original, Firebase e dados do app. Nao subir chaves de assinatura, keystores, senhas ou backups privados ao GitHub.
3. Revisar UX dos perfis, publicacoes e menu, ampliar funcoes apenas apos teste.
4. Confirmar se as regras Firestore da versao 2.0.2, incluindo `profiles/{uid}/posts/{postId}`, estao efetivamente publicadas e testadas (nao presumir).
5. A exclusao de conta depende da implantacao e teste da funcao de servidor; **nao declarar concluida** sem evidencia.
6. Testar login, perfil oficial, edicao, publicacoes, privacidade, seguidores, GPS, historico e atualizacao sobre a versao instalada antes de liberar uma release publica.
7. Usuario prefere **comando unico PowerShell**, nunca depender de `.cmd` (trava no Windows). Regras Firebase sempre **completas em bloco de codigo com botao Copiar**, nao apenas arquivos ou fragmentos.
8. Para cada nova release: tag `vX.Y.Z`, exatamente um APK oficial assinado, linha `Codigo: N`, certificacao e SHA-256 conferidos, verificar que GitHub Actions concluiu com sucesso e que `update.json` anuncia a nova versao.
9. Nao alterar versao publicada no manifesto manualmente sem validar o APK correspondente.

## Repositorio de distribuicao
https://github.com/SrDanvers/calisxtreme-atualizacoes

Observacao: este arquivo registra continuidade e progresso, **nao e um backup do projeto Android Studio nem do APK**. Mantenha os ZIPs, APKs e assinatura privada nos locais seguros originais.
