"""Point official l10n_cl commune xmlids at the historical res.city rows.

Odoo 20 loads the 346 Chilean communes from l10n_cl with xmlids
l10n_cl.city_cl_<n>. Databases coming from 19.0 already have those
communes as l10n_cl_counties.city_cl_<sii_code>. Loading both sets
would duplicate res.city and leave partner city_id on the legacy rows.
This script keeps the legacy row (and every foreign key on it) and
makes the official xmlid point at it.
"""

# (legacy xmlid name, official xmlid name)
CITY_XMLID_MAP = (
    ('city_cl_11201', 'city_cl_276'),  # Aisén -> Aysén
    ('city_cl_05602', 'city_cl_72'),
    ('city_cl_13502', 'city_cl_338'),
    ('city_cl_08314', 'city_cl_178'),
    ('city_cl_03302', 'city_cl_27'),  # Alto del Carmen -> Alto Del Carmen
    ('city_cl_01107', 'city_cl_11'),
    ('city_cl_10202', 'city_cl_254'),
    ('city_cl_04103', 'city_cl_32'),
    ('city_cl_09201', 'city_cl_221'),
    ('city_cl_12202', 'city_cl_289'),  # ANTÁRTICA -> Antártica
    ('city_cl_02101', 'city_cl_12'),
    ('city_cl_08302', 'city_cl_166'),
    ('city_cl_08202', 'city_cl_159'),
    ('city_cl_15101', 'city_cl_01'),
    ('city_cl_13402', 'city_cl_334'),
    ('city_cl_08402', 'city_cl_180'),
    ('city_cl_05402', 'city_cl_60'),
    ('city_cl_12201', 'city_cl_288'),  # Cabo de Hornos -> Cabo De Hornos
    ('city_cl_08303', 'city_cl_167'),
    ('city_cl_02201', 'city_cl_16'),
    ('city_cl_10102', 'city_cl_245'),
    ('city_cl_03102', 'city_cl_22'),
    ('city_cl_05502', 'city_cl_65'),  # Calera -> La Calera
    ('city_cl_13403', 'city_cl_335'),  # Calera de Tango -> Calera De Tango
    ('city_cl_05302', 'city_cl_56'),
    ('city_cl_15102', 'city_cl_02'),
    ('city_cl_01402', 'city_cl_06'),
    ('city_cl_04202', 'city_cl_37'),
    ('city_cl_08203', 'city_cl_160'),
    ('city_cl_09102', 'city_cl_201'),
    ('city_cl_05603', 'city_cl_73'),
    ('city_cl_05102', 'city_cl_46'),
    ('city_cl_10201', 'city_cl_253'),
    ('city_cl_05702', 'city_cl_78'),
    ('city_cl_07201', 'city_cl_126'),
    ('city_cl_13102', 'city_cl_296'),
    ('city_cl_13103', 'city_cl_297'),
    ('city_cl_10401', 'city_cl_270'),
    ('city_cl_03201', 'city_cl_24'),
    ('city_cl_07202', 'city_cl_127'),
    ('city_cl_06302', 'city_cl_107'),
    ('city_cl_08103', 'city_cl_148'),
    ('city_cl_11401', 'city_cl_282'),
    ('city_cl_08401', 'city_cl_179'),
    ('city_cl_08406', 'city_cl_184'),
    ('city_cl_06303', 'city_cl_108'),
    ('city_cl_09121', 'city_cl_220'),
    ('city_cl_10203', 'city_cl_255'),
    ('city_cl_11202', 'city_cl_277'),
    ('city_cl_08403', 'city_cl_181'),
    ('city_cl_10103', 'city_cl_246'),
    ('city_cl_11301', 'city_cl_279'),
    ('city_cl_06102', 'city_cl_84'),
    ('city_cl_08404', 'city_cl_182'),
    ('city_cl_11101', 'city_cl_274'),  # Coihaique -> Coyhaique
    ('city_cl_08405', 'city_cl_183'),
    ('city_cl_06103', 'city_cl_85'),
    ('city_cl_07402', 'city_cl_139'),
    ('city_cl_01403', 'city_cl_07'),
    ('city_cl_13301', 'city_cl_330'),
    ('city_cl_09202', 'city_cl_222'),
    ('city_cl_06104', 'city_cl_86'),
    ('city_cl_04302', 'city_cl_41'),
    ('city_cl_08101', 'city_cl_146'),
    ('city_cl_13104', 'city_cl_298'),
    ('city_cl_05103', 'city_cl_47'),
    ('city_cl_07102', 'city_cl_117'),
    ('city_cl_08204', 'city_cl_161'),
    ('city_cl_03101', 'city_cl_21'),
    ('city_cl_04102', 'city_cl_31'),
    ('city_cl_08102', 'city_cl_147'),
    ('city_cl_14102', 'city_cl_233'),
    ('city_cl_09103', 'city_cl_202'),
    ('city_cl_09203', 'city_cl_223'),
    ('city_cl_13503', 'city_cl_339'),
    ('city_cl_10204', 'city_cl_256'),  # Curaco de Vélez -> Curaco De Vélez
    ('city_cl_08205', 'city_cl_162'),
    ('city_cl_09104', 'city_cl_203'),
    ('city_cl_07103', 'city_cl_118'),
    ('city_cl_07301', 'city_cl_129'),
    ('city_cl_10205', 'city_cl_257'),
    ('city_cl_03202', 'city_cl_25'),  # Diego de Almagro -> Diego De Almagro
    ('city_cl_06105', 'city_cl_87'),
    ('city_cl_13105', 'city_cl_299'),
    ('city_cl_08407', 'city_cl_185'),
    ('city_cl_13602', 'city_cl_343'),
    ('city_cl_05604', 'city_cl_74'),
    ('city_cl_05605', 'city_cl_75'),
    ('city_cl_07104', 'city_cl_119'),
    ('city_cl_09204', 'city_cl_224'),
    ('city_cl_13106', 'city_cl_300'),
    ('city_cl_08104', 'city_cl_149'),
    ('city_cl_09105', 'city_cl_204'),
    ('city_cl_03303', 'city_cl_28'),
    ('city_cl_10104', 'city_cl_247'),
    ('city_cl_10105', 'city_cl_248'),
    ('city_cl_10402', 'city_cl_271'),
    ('city_cl_14202', 'city_cl_234'),
    ('city_cl_09106', 'city_cl_205'),
    ('city_cl_15202', 'city_cl_04'),
    ('city_cl_09107', 'city_cl_206'),
    ('city_cl_06106', 'city_cl_88'),
    ('city_cl_11203', 'city_cl_278'),
    ('city_cl_05503', 'city_cl_66'),
    ('city_cl_10403', 'city_cl_272'),  # Hualaihue -> Hualaihué
    ('city_cl_07302', 'city_cl_130'),  # Hualañé -> HualaÑé
    ('city_cl_08112', 'city_cl_157'),
    ('city_cl_08105', 'city_cl_150'),
    ('city_cl_01404', 'city_cl_08'),
    ('city_cl_03304', 'city_cl_29'),
    ('city_cl_13107', 'city_cl_301'),
    ('city_cl_04201', 'city_cl_36'),
    ('city_cl_13108', 'city_cl_302'),
    ('city_cl_01101', 'city_cl_05'),
    ('city_cl_13603', 'city_cl_344'),  # Isla de Maipo -> Isla De Maipo
    ('city_cl_05201', 'city_cl_54'),  # Isla de Pascua -> Isla De Pascua
    ('city_cl_05104', 'city_cl_48'),
    ('city_cl_13109', 'city_cl_303'),
    ('city_cl_05504', 'city_cl_67'),
    ('city_cl_06202', 'city_cl_101'),
    ('city_cl_13110', 'city_cl_304'),
    ('city_cl_14203', 'city_cl_236'),
    ('city_cl_11102', 'city_cl_275'),
    ('city_cl_13111', 'city_cl_305'),
    ('city_cl_12102', 'city_cl_285'),
    ('city_cl_04104', 'city_cl_33'),
    ('city_cl_08304', 'city_cl_168'),
    ('city_cl_05401', 'city_cl_59'),
    ('city_cl_13302', 'city_cl_331'),
    ('city_cl_14103', 'city_cl_237'),
    ('city_cl_13112', 'city_cl_306'),
    ('city_cl_13113', 'city_cl_307'),
    ('city_cl_06107', 'city_cl_89'),
    ('city_cl_13114', 'city_cl_308'),
    ('city_cl_04101', 'city_cl_30'),
    ('city_cl_14201', 'city_cl_235'),
    ('city_cl_09108', 'city_cl_207'),
    ('city_cl_08201', 'city_cl_158'),
    ('city_cl_07303', 'city_cl_131'),
    ('city_cl_05505', 'city_cl_68'),
    ('city_cl_07401', 'city_cl_138'),
    ('city_cl_06203', 'city_cl_102'),
    ('city_cl_10107', 'city_cl_250'),
    ('city_cl_05703', 'city_cl_79'),  # se conserva "Llay Llay" (oficial: Llaillay)
    ('city_cl_13115', 'city_cl_309'),
    ('city_cl_13116', 'city_cl_310'),
    ('city_cl_06304', 'city_cl_109'),
    ('city_cl_09109', 'city_cl_208'),  # se conserva "Loncoche" (oficial: Loncoch)
    ('city_cl_07403', 'city_cl_140'),
    ('city_cl_09205', 'city_cl_225'),
    ('city_cl_13117', 'city_cl_311'),
    ('city_cl_08206', 'city_cl_163'),  # Los Alamos -> Los Álamos
    ('city_cl_05301', 'city_cl_55'),
    ('city_cl_08301', 'city_cl_165'),  # Los Angeles -> Los Ángeles
    ('city_cl_14104', 'city_cl_238'),
    ('city_cl_10106', 'city_cl_249'),
    ('city_cl_09206', 'city_cl_226'),
    ('city_cl_04203', 'city_cl_38'),
    ('city_cl_08106', 'city_cl_151'),
    ('city_cl_09207', 'city_cl_227'),
    ('city_cl_06108', 'city_cl_90'),
    ('city_cl_13118', 'city_cl_312'),
    ('city_cl_14105', 'city_cl_239'),
    ('city_cl_13119', 'city_cl_313'),
    ('city_cl_06109', 'city_cl_91'),
    ('city_cl_06204', 'city_cl_103'),  # Marchihue -> Marchigüe
    ('city_cl_02302', 'city_cl_20'),
    ('city_cl_13504', 'city_cl_340'),
    ('city_cl_14106', 'city_cl_240'),
    ('city_cl_07105', 'city_cl_120'),
    ('city_cl_10108', 'city_cl_251'),
    ('city_cl_02102', 'city_cl_13'),
    ('city_cl_09110', 'city_cl_209'),
    ('city_cl_13501', 'city_cl_337'),
    ('city_cl_07304', 'city_cl_132'),
    ('city_cl_04303', 'city_cl_42'),
    ('city_cl_06110', 'city_cl_92'),
    ('city_cl_08305', 'city_cl_169'),
    ('city_cl_08306', 'city_cl_170'),
    ('city_cl_06305', 'city_cl_110'),
    ('city_cl_12401', 'city_cl_293'),
    ('city_cl_06205', 'city_cl_104'),
    ('city_cl_08307', 'city_cl_171'),
    ('city_cl_08408', 'city_cl_186'),
    ('city_cl_08409', 'city_cl_187'),
    ('city_cl_05506', 'city_cl_69'),
    ('city_cl_09111', 'city_cl_210'),
    ('city_cl_13120', 'city_cl_314'),
    ('city_cl_11302', 'city_cl_280'),  # Ohiggins -> O'Higgins
    ('city_cl_06111', 'city_cl_93'),
    ('city_cl_02202', 'city_cl_17'),  # Ollague -> Ollagüe
    ('city_cl_05507', 'city_cl_70'),
    ('city_cl_10301', 'city_cl_263'),
    ('city_cl_04301', 'city_cl_40'),
    ('city_cl_13604', 'city_cl_345'),
    ('city_cl_09112', 'city_cl_211'),
    ('city_cl_04105', 'city_cl_34'),
    ('city_cl_14107', 'city_cl_241'),
    ('city_cl_13404', 'city_cl_336'),
    ('city_cl_10404', 'city_cl_273'),
    ('city_cl_06306', 'city_cl_111'),
    ('city_cl_14108', 'city_cl_242'),
    ('city_cl_05704', 'city_cl_80'),
    ('city_cl_05403', 'city_cl_61'),
    ('city_cl_06206', 'city_cl_105'),
    ('city_cl_07404', 'city_cl_141'),
    ('city_cl_13121', 'city_cl_315'),
    ('city_cl_07106', 'city_cl_121'),
    ('city_cl_07203', 'city_cl_128'),
    ('city_cl_08410', 'city_cl_188'),
    ('city_cl_13605', 'city_cl_346'),
    ('city_cl_13122', 'city_cl_316'),
    ('city_cl_07107', 'city_cl_122'),
    ('city_cl_08107', 'city_cl_152'),
    ('city_cl_06307', 'city_cl_112'),
    ('city_cl_09113', 'city_cl_212'),
    ('city_cl_05404', 'city_cl_62'),
    ('city_cl_06112', 'city_cl_94'),
    ('city_cl_01405', 'city_cl_09'),
    ('city_cl_06113', 'city_cl_95'),
    ('city_cl_06201', 'city_cl_100'),
    ('city_cl_08411', 'city_cl_189'),
    ('city_cl_13202', 'city_cl_328'),
    ('city_cl_09114', 'city_cl_213'),
    ('city_cl_06308', 'city_cl_113'),
    ('city_cl_08412', 'city_cl_190'),
    ('city_cl_12301', 'city_cl_290'),
    ('city_cl_01401', 'city_cl_10'),
    ('city_cl_12302', 'city_cl_291'),
    ('city_cl_13123', 'city_cl_317'),
    ('city_cl_05105', 'city_cl_49'),
    ('city_cl_09115', 'city_cl_214'),
    ('city_cl_13124', 'city_cl_318'),
    ('city_cl_13201', 'city_cl_327'),
    ('city_cl_10101', 'city_cl_244'),
    ('city_cl_10302', 'city_cl_264'),
    ('city_cl_10109', 'city_cl_252'),
    ('city_cl_06309', 'city_cl_114'),
    ('city_cl_04304', 'city_cl_43'),
    ('city_cl_12101', 'city_cl_284'),
    ('city_cl_10206', 'city_cl_258'),
    ('city_cl_09208', 'city_cl_228'),
    ('city_cl_10303', 'city_cl_265'),
    ('city_cl_05705', 'city_cl_81'),
    ('city_cl_15201', 'city_cl_03'),
    ('city_cl_10304', 'city_cl_266'),
    ('city_cl_10207', 'city_cl_259'),
    ('city_cl_10208', 'city_cl_260'),
    ('city_cl_10209', 'city_cl_261'),
    ('city_cl_08308', 'city_cl_172'),
    ('city_cl_13125', 'city_cl_319'),
    ('city_cl_08309', 'city_cl_173'),
    ('city_cl_08413', 'city_cl_191'),
    ('city_cl_05501', 'city_cl_64'),
    ('city_cl_05106', 'city_cl_50'),
    ('city_cl_10210', 'city_cl_262'),
    ('city_cl_06114', 'city_cl_96'),  # Quinta de Tilcoco -> Quinta De Tilcoco
    ('city_cl_13126', 'city_cl_320'),
    ('city_cl_05107', 'city_cl_51'),
    ('city_cl_08414', 'city_cl_192'),
    ('city_cl_06101', 'city_cl_83'),
    ('city_cl_08415', 'city_cl_193'),  # Ranquil -> Ránquil
    ('city_cl_07305', 'city_cl_133'),
    ('city_cl_13127', 'city_cl_321'),
    ('city_cl_09209', 'city_cl_229'),
    ('city_cl_13128', 'city_cl_322'),
    ('city_cl_06115', 'city_cl_97'),
    ('city_cl_06116', 'city_cl_98'),  # Requinoa -> Requínoa
    ('city_cl_07405', 'city_cl_142'),
    ('city_cl_05303', 'city_cl_57'),
    ('city_cl_14204', 'city_cl_243'),
    ('city_cl_07108', 'city_cl_123'),
    ('city_cl_04305', 'city_cl_44'),
    ('city_cl_11402', 'city_cl_283'),
    ('city_cl_10305', 'city_cl_267'),
    ('city_cl_12103', 'city_cl_286'),
    ('city_cl_07306', 'city_cl_134'),
    ('city_cl_09116', 'city_cl_215'),
    ('city_cl_07307', 'city_cl_135'),
    ('city_cl_04204', 'city_cl_39'),
    ('city_cl_05601', 'city_cl_71'),
    ('city_cl_13401', 'city_cl_333'),
    ('city_cl_08416', 'city_cl_194'),
    ('city_cl_07109', 'city_cl_124'),
    ('city_cl_05304', 'city_cl_58'),
    ('city_cl_08417', 'city_cl_195'),
    ('city_cl_05701', 'city_cl_77'),
    ('city_cl_06301', 'city_cl_106'),
    ('city_cl_12104', 'city_cl_287'),
    ('city_cl_08418', 'city_cl_196'),
    ('city_cl_07406', 'city_cl_143'),
    ('city_cl_13129', 'city_cl_323'),
    ('city_cl_13203', 'city_cl_329'),  # San José de Maipo -> San José De Maipo
    ('city_cl_10306', 'city_cl_268'),  # San Juan de la Costa -> San Juan De La Costa
    ('city_cl_13130', 'city_cl_324'),
    ('city_cl_08419', 'city_cl_197'),
    ('city_cl_10307', 'city_cl_269'),
    ('city_cl_13505', 'city_cl_341'),
    ('city_cl_02203', 'city_cl_18'),  # San Pedro de Atacama -> San Pedro De Atacama
    ('city_cl_08108', 'city_cl_153'),
    ('city_cl_07110', 'city_cl_125'),
    ('city_cl_13131', 'city_cl_325'),
    ('city_cl_08310', 'city_cl_174'),
    ('city_cl_08311', 'city_cl_175'),
    ('city_cl_06310', 'city_cl_115'),
    ('city_cl_08109', 'city_cl_154'),
    ('city_cl_05706', 'city_cl_82'),
    ('city_cl_13101', 'city_cl_295'),
    ('city_cl_05606', 'city_cl_76'),
    ('city_cl_06117', 'city_cl_99'),
    ('city_cl_02103', 'city_cl_14'),
    ('city_cl_13601', 'city_cl_342'),
    ('city_cl_07101', 'city_cl_116'),
    ('city_cl_08110', 'city_cl_155'),
    ('city_cl_02104', 'city_cl_15'),
    ('city_cl_09101', 'city_cl_200'),
    ('city_cl_07308', 'city_cl_136'),
    ('city_cl_09117', 'city_cl_216'),
    ('city_cl_03103', 'city_cl_23'),
    ('city_cl_13303', 'city_cl_332'),  # Til til -> Til Til
    ('city_cl_12303', 'city_cl_292'),
    ('city_cl_08207', 'city_cl_164'),  # Tirua -> Tirúa
    ('city_cl_02301', 'city_cl_19'),
    ('city_cl_09118', 'city_cl_217'),
    ('city_cl_08111', 'city_cl_156'),
    ('city_cl_12402', 'city_cl_294'),  # Torres del Paine -> Torres Del Paine
    ('city_cl_11303', 'city_cl_281'),
    ('city_cl_09210', 'city_cl_230'),
    ('city_cl_08420', 'city_cl_198'),  # Trehuaco -> Treguaco
    ('city_cl_08312', 'city_cl_176'),
    ('city_cl_14101', 'city_cl_232'),
    ('city_cl_03301', 'city_cl_26'),
    ('city_cl_05101', 'city_cl_45'),
    ('city_cl_07309', 'city_cl_137'),
    ('city_cl_09211', 'city_cl_231'),
    ('city_cl_04106', 'city_cl_35'),
    ('city_cl_09119', 'city_cl_218'),
    ('city_cl_07407', 'city_cl_144'),
    ('city_cl_05108', 'city_cl_52'),
    ('city_cl_09120', 'city_cl_219'),
    ('city_cl_05109', 'city_cl_53'),  # Viña del Mar -> Viña Del Mar
    ('city_cl_13132', 'city_cl_326'),
    ('city_cl_07408', 'city_cl_145'),
    ('city_cl_08313', 'city_cl_177'),
    ('city_cl_08421', 'city_cl_199'),
    ('city_cl_05405', 'city_cl_63'),
)


def _xmlid(cr, module, name):
    cr.execute(
        """
        SELECT id, res_id
          FROM ir_model_data
         WHERE module = %s
           AND name = %s
           AND model = 'res.city'
        """,
        (module, name),
    )
    return cr.fetchone()


def _sql_ident(name):
    parts = name.split(".")
    if not parts or not all(part.replace("_", "").isalnum() for part in parts):
        raise ValueError("Unexpected SQL identifier: %s" % name)
    return ".".join('"%s"' % part for part in parts)


def _repoint_city(cr, source_id, target_id):
    """Move foreign keys off the duplicate official city."""
    cr.execute(
        """
        SELECT c.conrelid::regclass::text AS table_name,
               a.attname AS column_name
          FROM pg_constraint c
          JOIN pg_attribute a
            ON a.attrelid = c.conrelid
           AND a.attnum = ANY (c.conkey)
         WHERE c.confrelid = 'res_city'::regclass
           AND c.contype = 'f'
        """
    )
    for table_name, column_name in cr.fetchall():
        table_sql = _sql_ident(table_name)
        column_sql = _sql_ident(column_name)
        cr.execute(
            f'UPDATE {table_sql} SET {column_sql} = %s WHERE {column_sql} = %s',
            (target_id, source_id),
        )


# Official xmlids whose commune name stays as loaded by l10n_cl_counties.
KEEP_LEGACY_NAMES = frozenset({
    'city_cl_79',   # Llay Llay, not Llaillay
    'city_cl_208',  # Loncoche, not Loncoch
})


def _keep_legacy_name(cr, official_name):
    """Stop a later l10n_cl update from overwriting the historical name."""
    if official_name not in KEEP_LEGACY_NAMES:
        return
    cr.execute(
        """
        UPDATE ir_model_data
           SET noupdate = TRUE
         WHERE module = 'l10n_cl'
           AND name = %s
           AND model = 'res.city'
        """,
        (official_name,),
    )


def migrate(cr, version):
    if not version:
        return
    for legacy_name, official_name in CITY_XMLID_MAP:
        legacy = _xmlid(cr, 'l10n_cl_counties', legacy_name)
        official = _xmlid(cr, 'l10n_cl', official_name)
        if not legacy:
            continue
        keep_name = official_name in KEEP_LEGACY_NAMES
        if official and legacy[1] != official[1]:
            _repoint_city(cr, official[1], legacy[1])
            cr.execute(
                """
                UPDATE res_city AS legacy
                   SET name = CASE WHEN %s THEN legacy.name ELSE official.name END,
                       state_id = official.state_id,
                       country_id = official.country_id
                  FROM res_city AS official
                 WHERE legacy.id = %s
                   AND official.id = %s
                """,
                (keep_name, legacy[1], official[1]),
            )
            cr.execute(
                "UPDATE ir_model_data SET res_id = %s WHERE id = %s",
                (legacy[1], official[0]),
            )
            cr.execute("DELETE FROM res_city WHERE id = %s", (official[1],))
            cr.execute("DELETE FROM ir_model_data WHERE id = %s", (legacy[0],))
        elif official and legacy[1] == official[1]:
            cr.execute("DELETE FROM ir_model_data WHERE id = %s", (legacy[0],))
        else:
            cr.execute(
                """
                UPDATE ir_model_data
                   SET module = 'l10n_cl',
                       name = %s
                 WHERE id = %s
                """,
                (official_name, legacy[0]),
            )
        _keep_legacy_name(cr, official_name)
