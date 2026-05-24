# BMyA Contributor License Agreement (CLA)

This directory contains the Contributor License Agreements (CLAs) for all contributions to BMyA repositories — public (e.g. `bmya/odoo-bmya`) and private (e.g. `bmya/bmya-enterprise`, `bmya/bmya-tools`, `bmya/bmya-ai`, `bmya/bmya-crm`, client repos, etc.).

Every commit author whose contribution lands in a BMyA repository must be registered here, either as an individual signatory under [`individual/`](individual/) or as part of a corporate signatory's roster under [`corporate/`](corporate/). The CI check `legal/cla` enforces this on every pull request.

> Este directorio contiene los Acuerdos de Licencia de Colaborador (CLAs) para todas las contribuciones a repositorios BMyA — públicos (ej. `bmya/odoo-bmya`) y privados (ej. `bmya/bmya-enterprise`, `bmya/bmya-tools`, `bmya/bmya-ai`, `bmya/bmya-crm`, repos de clientes, etc.).
>
> Cada autor de commit cuya contribución llegue a un repositorio BMyA debe estar registrado aquí, ya sea como firmante individual en [`individual/`](individual/) o como parte del listado de un firmante corporativo en [`corporate/`](corporate/). El check de CI `legal/cla` lo valida en cada pull request.

---

## How to sign / Cómo firmar

### If you are an individual / Si firmas como persona

1. Read the [Individual Contributor License Agreement](icla-1.0.md) (ICLA v1.0).
2. Open a pull request on `bmya/odoo-bmya` targeting the `16.0` branch, adding **two files** under [`individual/`](individual/):
   - `<your-github-login>.md` — copy of [`individual/TEMPLATE.md`](individual/TEMPLATE.md), filled with your signature block.
   - `<your-github-login>.yaml` — copy of [`individual/TEMPLATE.yaml`](individual/TEMPLATE.yaml), filled with your machine-readable data (GitHub login + authorized emails).
3. Once merged, your signature propagates automatically forward to `17.0`, `18.0`, etc. via the BMyA forward-port bot. After the cascade completes, your future contributions to any BMyA repo on those branches will pass the `legal/cla` check.

> 1. Lee el [Acuerdo de Licencia de Colaborador Individual](icla-1.0.md) (ICLA v1.0).
> 2. Abre un pull request en `bmya/odoo-bmya` apuntando a la rama `16.0`, agregando **dos archivos** en [`individual/`](individual/):
>    - `<tu-login-github>.md` — copia de [`individual/TEMPLATE.md`](individual/TEMPLATE.md), completa el bloque de firma.
>    - `<tu-login-github>.yaml` — copia de [`individual/TEMPLATE.yaml`](individual/TEMPLATE.yaml), completa con tus datos parseables (login de GitHub + emails autorizados).
> 3. Una vez mergeado, tu firma se propaga automáticamente hacia adelante a `17.0`, `18.0`, etc. vía el forward-port bot de BMyA. Cuando termine la cascada, tus contribuciones futuras a cualquier repo BMyA en esas ramas pasarán el check `legal/cla`.

### If you contribute on behalf of a company / Si firmas en nombre de una empresa

1. Read the [Corporate Contributor License Agreement](ccla-1.0.md) (CCLA v1.0). Pay particular attention to the OPL-1 clause that applies to contributions to private BMyA repositories.
2. The authorized signatory of your company opens a pull request on `bmya/odoo-bmya` targeting `16.0`, adding **two files** under [`corporate/`](corporate/):
   - `<company-slug>.md` — copy of [`corporate/TEMPLATE.md`](corporate/TEMPLATE.md), filled with the corporate signature.
   - `<company-slug>.yaml` — copy of [`corporate/TEMPLATE.yaml`](corporate/TEMPLATE.yaml), with the signatory data and the full list of authorized contributors.
3. Adding or removing contributors from the roster later is done by the same signatory through a new pull request editing only the `.yaml` file.

> 1. Lee el [Acuerdo de Licencia de Colaborador Corporativo](ccla-1.0.md) (CCLA v1.0). Presta especial atención a la cláusula OPL-1 que aplica a contribuciones a repos privados de BMyA.
> 2. El firmante autorizado de tu empresa abre un pull request en `bmya/odoo-bmya` apuntando a `16.0`, agregando **dos archivos** en [`corporate/`](corporate/):
>    - `<slug-empresa>.md` — copia de [`corporate/TEMPLATE.md`](corporate/TEMPLATE.md), completa con la firma corporativa.
>    - `<slug-empresa>.yaml` — copia de [`corporate/TEMPLATE.yaml`](corporate/TEMPLATE.yaml), con los datos del firmante y la lista completa de contribuyentes autorizados.
> 3. Las altas o bajas de contribuyentes posteriores las hace el mismo firmante a través de un nuevo pull request editando sólo el archivo `.yaml`.

---

## File convention / Convención de archivos

| File | Purpose |
|---|---|
| `icla-1.0.md` / `ccla-1.0.md` | Canonical legal text (English + Spanish). Stable; rarely changes |
| `<entity>.md` | Signed declaration referencing the canonical text. Immutable once signed |
| `<entity>.yaml` | Machine-readable roster. Edited by signatory when adding/removing contributors |
| `TEMPLATE.md` / `TEMPLATE.yaml` | Templates to copy and fill |

The CI parser only reads `*.yaml` files; the `.md` files are the legally binding artifacts.

---

## What the `legal/cla` check validates / Qué valida el check `legal/cla`

For each commit in a pull request, the check:

1. Resolves the **target branch's version** of `bmya/odoo-bmya` (16.0/17.0/18.0/etc.) and reads the CLA roster from `doc/cla/` on that branch.
2. Looks up the commit author's GitHub login. **It must be registered** (individual `.yaml` filename or corporate `contributors[].github`).
3. Validates that the commit's author email matches one of the **authorized emails** listed for that login.
4. Fails the PR with a precise message indicating what's missing if either check fails.

> Para cada commit en un pull request, el check:
>
> 1. Resuelve la **versión de la rama target** de `bmya/odoo-bmya` (16.0/17.0/18.0/etc.) y lee el registro CLA de `doc/cla/` en esa rama.
> 2. Busca el login de GitHub del autor del commit. **Debe estar registrado** (filename del `.yaml` individual o `contributors[].github` del corporate).
> 3. Valida que el email del commit coincida con uno de los **emails autorizados** listados para ese login.
> 4. Falla el PR con un mensaje específico indicando qué falta si cualquiera de los dos checks falla.

### Bypasses

- Whitelisted bots: `robbmya`, `dependabot[bot]`, `github-actions[bot]`, the BMyA forward-port bot.
- Self-signup: pull requests that only add `doc/cla/individual/<author-login>.{md,yaml}` are exempt — this is how new individual contributors can sign without being blocked by their own first PR.

> - Bots en lista blanca: `robbmya`, `dependabot[bot]`, `github-actions[bot]`, el forward-port bot de BMyA.
> - Auto-firma: los pull requests que sólo agregan `doc/cla/individual/<author-login>.{md,yaml}` están exentos — así es como nuevos contribuyentes individuales pueden firmar sin ser bloqueados por su propio primer PR.

---

## FAQ

### Why a CLA at all? / ¿Por qué un CLA?

To establish a clear, non-repudiable record that each contributor intended to contribute under specific terms and had the right to do so. This protects the BMyA project, its users, and the contributors themselves in case of legal disputes.

> Para establecer un registro claro y no repudiable de que cada contribuyente quiso contribuir bajo términos específicos y tenía derecho a hacerlo. Esto protege al proyecto BMyA, a sus usuarios y a los propios contribuyentes en caso de disputas legales.

### Why register both GitHub login *and* email? / ¿Por qué registrar login de GitHub *y* email?

Many developers maintain a corporate GitHub account (e.g. `company-user`) alongside a personal one (e.g. `personal-user`). Committing with the wrong account breaks the legal chain. By requiring **both** the login and the commit email to match the roster, accidental commits from the wrong identity are blocked at CI time.

> Muchos desarrolladores mantienen una cuenta de GitHub corporativa (ej. `usuario-empresa`) en paralelo a una personal (ej. `usuario-personal`). Cometer con la cuenta equivocada rompe la cadena legal. Al requerir que **ambos**, el login y el email del commit, coincidan con el registro, los commits accidentales desde la identidad equivocada se bloquean en CI.

### What about contributions to forks / external projects? / ¿Qué pasa con contribuciones a forks o proyectos externos?

The `legal/cla` check only runs on pull requests targeting `bmya/*` repositories. Contributions to upstream Odoo or to other organizations are out of scope.

> El check `legal/cla` sólo corre en pull requests apuntando a repositorios `bmya/*`. Las contribuciones al upstream Odoo o a otras organizaciones están fuera de alcance.

---

For questions, contact: `cla@bmya.cl`
