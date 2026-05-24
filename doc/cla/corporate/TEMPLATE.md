<!--
INSTRUCTIONS / INSTRUCCIONES

1. Copy this file to `<company-slug>.md` (lowercase, ASCII, hyphens for spaces).
   Examples: `blanco-martin-y-asociados.md`, `bmya.md`, `adhoc.md`.

   Copia este archivo a `<slug-empresa>.md` (minúsculas, ASCII, guiones para
   espacios). Ejemplos: `blanco-martin-y-asociados.md`, `bmya.md`, `adhoc.md`.

2. Also copy `TEMPLATE.yaml` to `<company-slug>.yaml` with the same slug and
   fill it with signatory + contributors data.

   Copia también `TEMPLATE.yaml` a `<slug-empresa>.yaml` con el mismo slug y
   complétalo con los datos del firmante + contribuyentes.

3. Replace the placeholders below with real values, then remove this
   instruction block.

   Reemplaza los placeholders abajo con datos reales, luego elimina este
   bloque de instrucciones.

4. The signatory MUST be a person authorized to bind the Corporation
   (e.g. Director, Legal Representative, CEO).

   El firmante DEBE ser una persona autorizada a obligar a la Corporación
   (ej. Director, Representante Legal, CEO).

5. Open a pull request on `bmya/odoo-bmya` targeting `16.0`. After merge,
   the BMyA forward-port bot propagates the signature to 17.0, 18.0, etc.

   Abre un pull request en `bmya/odoo-bmya` apuntando a `16.0`. Después del
   merge, el forward-port bot de BMyA propaga la firma a 17.0, 18.0, etc.

6. To add or remove contributors later, open a follow-up PR editing ONLY the
   `.yaml` file. The signed `.md` remains immutable.

   Para agregar o remover contribuyentes después, abre un PR posterior
   editando SÓLO el archivo `.yaml`. El `.md` firmado permanece inmutable.
-->

<COUNTRY>, <YYYY-MM-DD>

<COMPANY LEGAL NAME> agrees to the terms of the BMyA Corporate Contributor
License Agreement v1.0 ([ccla-1.0.md](../ccla-1.0.md)), including the
**Section 9 OPL-1 Clause** that applies to Contributions to BMyA's private
repositories.

I declare that I am authorized and able to make this agreement and sign this
declaration on behalf of the Corporation.

Signed,

<SIGNATORY NAME> <signatory_email> https://github.com/<signatory-github-login>

Corporation name: <COMPANY LEGAL NAME>
Corporation address: <ADDRESS LINE 1>
                     <ADDRESS LINE 2>
Country: <COUNTRY>
Point of contact: <SIGNATORY NAME>
Title: <SIGNATORY ROLE, e.g. Director - Representante Legal>
Email: <signatory_email>
Telephone: <+CC PHONE>

The current list of authorized contributors for this Corporation is maintained
in the companion file [`<company-slug>.yaml`](./<company-slug>.yaml) and may be
updated by the signatory above through subsequent pull requests.

---

<COMPANY LEGAL NAME> acepta los términos del Acuerdo de Licencia de Colaborador
Corporativo de BMyA v1.0 ([ccla-1.0.md](../ccla-1.0.md)), incluyendo la
**Cláusula Sección 9 OPL-1** que aplica a Contribuciones a los repositorios
privados de BMyA.

Declaro que estoy autorizado/a y en condiciones de celebrar este acuerdo y
firmar esta declaración en nombre de la Corporación.

Firmado,

<NOMBRE DEL FIRMANTE> <signatory_email> https://github.com/<signatory-github-login>

Nombre de la Corporación: <NOMBRE LEGAL DE LA EMPRESA>
Dirección: <DIRECCIÓN LÍNEA 1>
           <DIRECCIÓN LÍNEA 2>
País: <PAÍS>
Punto de contacto: <NOMBRE DEL FIRMANTE>
Cargo: <CARGO, ej. Director - Representante Legal>
Email: <signatory_email>
Teléfono: <+CC TELÉFONO>

El listado actual de contribuyentes autorizados de esta Corporación se mantiene
en el archivo acompañante [`<slug-empresa>.yaml`](./<slug-empresa>.yaml) y puede
ser actualizado por el firmante a través de pull requests posteriores.
