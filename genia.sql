/*
 Navicat Premium Data Transfer

 Source Server         : genia
 Source Server Type    : PostgreSQL
 Source Server Version : 100004 (100004)
 Source Host           : localhost:5432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100004 (100004)
 File Encoding         : 65001

 Date: 17/10/2025 18:56:59
*/


-- ----------------------------
-- Sequence structure for assets_asset_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."assets_asset_id_seq";
CREATE SEQUENCE "public"."assets_asset_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for brands_brand_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."brands_brand_id_seq";
CREATE SEQUENCE "public"."brands_brand_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_conf_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."config_conf_id_seq";
CREATE SEQUENCE "public"."config_conf_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_conf_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."config_conf_id_seq1";
CREATE SEQUENCE "public"."config_conf_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for exclusiones_exsite_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."exclusiones_exsite_id_seq";
CREATE SEQUENCE "public"."exclusiones_exsite_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for exclusiones_exsite_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."exclusiones_exsite_id_seq1";
CREATE SEQUENCE "public"."exclusiones_exsite_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for links_link_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."links_link_id_seq";
CREATE SEQUENCE "public"."links_link_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for sitemap_site_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."sitemap_site_id_seq";
CREATE SEQUENCE "public"."sitemap_site_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for sitemap_site_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."sitemap_site_id_seq1";
CREATE SEQUENCE "public"."sitemap_site_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_user_id_seq";
CREATE SEQUENCE "public"."users_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_user_id_seq1
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_user_id_seq1";
CREATE SEQUENCE "public"."users_user_id_seq1" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS "public"."article";
CREATE TABLE "public"."article" (
  "article_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "article_title" varchar(255) COLLATE "pg_catalog"."default",
  "article_content" text COLLATE "pg_catalog"."default",
  "article_keyword" varchar(255) COLLATE "pg_catalog"."default",
  "article_estado" int4,
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of article
-- ----------------------------

-- ----------------------------
-- Table structure for assets
-- ----------------------------
DROP TABLE IF EXISTS "public"."assets";
CREATE TABLE "public"."assets" (
  "asset_id" int4 NOT NULL DEFAULT nextval('assets_asset_id_seq'::regclass),
  "asset_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "asset_src" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "asset_value" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "asset_type" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "asset_ext" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "asset_fecha" timestamp(0) NOT NULL,
  "asset_estado" int4,
  "asset_tags" text COLLATE "pg_catalog"."default",
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of assets
-- ----------------------------
INSERT INTO "public"."assets" VALUES (4, 'fondo_04-250x250.jpg', '20250903_usuario_ejemplo_57e5a44cc9c04bdc8d7b32d2a15e5ff7.jpg', '20250903_usuario_ejemplo_57e5a44cc9c04bdc8d7b32d2a15e5ff7', 'images', 'jpg', '2025-09-03 16:53:45', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (46, 'fondo_06-300x600.jpg', '20250915_usuario_ejemplo_e9023d5d5dac4a809ca8bdc1cf47085e.jpg', '20250915_usuario_ejemplo_e9023d5d5dac4a809ca8bdc1cf47085e', 'images', 'jpg', '2025-09-15 17:58:58', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (40, 'fondo_04-250x250.jpg', '20250911_usuario_ejemplo_72dce30736e141f0a4d33524ab59cbc2.jpg', '20250911_usuario_ejemplo_72dce30736e141f0a4d33524ab59cbc2', 'images', 'jpg', '2025-09-11 16:09:31', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (39, 'fondo_06-300x600.jpg', '20250911_usuario_ejemplo_b34c73bddd604a02aebfedc2dca1a76a.jpg', '20250911_usuario_ejemplo_b34c73bddd604a02aebfedc2dca1a76a', 'images', 'jpg', '2025-09-11 16:09:31', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (14, '#ff7f50', '', '#ff7f50', 'colors', '', '2025-09-05 13:09:36', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (19, '#0077b6', '', '#0077b6', 'colors', '', '2025-09-05 15:35:30', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (15, '#0098c7', '', '#0098c7', 'colors', '', '2025-09-05 15:43:13', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (18, '#0098c7', '', '#0098c7', 'colors', '', '2025-09-05 15:43:13', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (17, '#ff7f50', '', '#ff7f50', 'colors', '', '2025-09-11 11:23:08', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (16, '#0077b6', '', '#0077b6', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (31, '#eef1f4', '', '#eef1f4', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (35, '#e9c46a', '', '#e9c46a', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (30, '#eef1f4', '', '#eef1f4', 'colors', '', '2025-09-11 14:16:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (32, '#eef1f4', '', '#eef1f4', 'colors', '', '2025-09-11 14:16:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (33, '#eef1f4', '', '#eef1f4', 'colors', '', '2025-09-11 14:16:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (34, '#eef1f4', '', '#eef1f4', 'colors', '', '2025-09-11 14:16:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (29, '#dc143c', '', '#dc143c', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (43, '#00b4d8', '', '#00b4d8', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (49, '#7500fb', '', '#7500fb', 'colors', '', '2025-09-17 15:14:01', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (13, 'pleasantcries.otf', '20250904_usuario_ejemplo_58aed5e868084455ad04f46314ce2762.otf', '20250904_usuario_ejemplo_58aed5e868084455ad04f46314ce2762', 'fonts', 'otf', '2025-09-04 15:47:22', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (41, 'YourHighschoolCrush-Regular.otf', '20250911_usuario_ejemplo_b771dc9a3a594ab6a1a5d1355e1d49ed.otf', '20250911_usuario_ejemplo_b771dc9a3a594ab6a1a5d1355e1d49ed', 'fonts', 'otf', '2025-09-11 16:09:31', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (42, 'Mango.otf', '20250915_usuario_ejemplo_9df5fcbd552b43499b6d5a6eebaab334.otf', '20250915_usuario_ejemplo_9df5fcbd552b43499b6d5a6eebaab334', 'fonts', 'otf', '2025-09-15 10:58:24', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (45, 'NewWildWordsRoman.TTF', '20250915_usuario_ejemplo_662b78af94514530a62ec99fa90b9e6b.TTF', '20250915_usuario_ejemplo_662b78af94514530a62ec99fa90b9e6b', 'fonts', 'TTF', '2025-09-15 17:58:12', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (5, 'El Mundo Telco.pdf', '20250903_usuario_ejemplo_70bce5cc3b9840feb0531c3c0b2e9a36.pdf', '20250903_usuario_ejemplo_70bce5cc3b9840feb0531c3c0b2e9a36', 'files', 'pdf', '2025-09-03 17:04:46', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (6, 'test.xlsx', '20250903_usuario_ejemplo_74b3e4bb1f424cf98c7755eb9c86e0a9.xlsx', '20250903_usuario_ejemplo_74b3e4bb1f424cf98c7755eb9c86e0a9', 'files', 'xlsx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (7, 'test.docx', '20250903_usuario_ejemplo_412918a5c84f4a18b8d3245b347d279d.docx', '20250903_usuario_ejemplo_412918a5c84f4a18b8d3245b347d279d', 'files', 'docx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (8, 'test.pptx', '20250903_usuario_ejemplo_a8ff221e745f460d93b2285475b63198.pptx', '20250903_usuario_ejemplo_a8ff221e745f460d93b2285475b63198', 'files', 'pptx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (12, 'test.docx', '20250904_usuario_ejemplo_6bba32ae19cd470eb4725968fc2e2476.docx', '20250904_usuario_ejemplo_6bba32ae19cd470eb4725968fc2e2476', 'files', 'docx', '2025-09-04 11:08:41', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (37, 'test.pptx', '20250911_usuario_ejemplo_091f02ab90cf4511bc59c86102cd307a.pptx', '20250911_usuario_ejemplo_091f02ab90cf4511bc59c86102cd307a', 'files', 'pptx', '2025-09-11 15:50:45', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (38, 'test.xlsx', '20250911_usuario_ejemplo_55f556cc25d94d16b91c6e32bb6a29e5.xlsx', '20250911_usuario_ejemplo_55f556cc25d94d16b91c6e32bb6a29e5', 'files', 'xlsx', '2025-09-11 15:50:45', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (9, 'test.docx', '20250903_usuario_ejemplo_e192af30959c4f3faa45f387c0a03394.docx', '20250903_usuario_ejemplo_e192af30959c4f3faa45f387c0a03394', 'files', 'docx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (63, 'photo_girl.png', '20250918_usuario_ejemplo_1e28fbb4b5904fdaa373277240a8e075.png', '20250918_usuario_ejemplo_1e28fbb4b5904fdaa373277240a8e075', 'images', 'png', '2025-09-18 15:22:28', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (64, 'Banner-Titulo-2300x450-Desktop-Claro-5G.jpg', '20250918_usuario_ejemplo_abb30967fb414ddbb64e97f3ee6994fd.jpg', '20250918_usuario_ejemplo_abb30967fb414ddbb64e97f3ee6994fd', 'images', 'jpg', '2025-09-18 15:22:29', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (50, 'Reporte.pdf', '20250917_usuario_ejemplo_51126b7be3c24cb79bb464fe5b8d1071.pdf', '20250917_usuario_ejemplo_51126b7be3c24cb79bb464fe5b8d1071', 'files', 'pdf', '2025-09-17 15:22:55', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (23, 'fondo_06-300x600.jpg', '20250905_usuario_ejemplo_2717ffa3b95c4679a2cf159215b99238.jpg', '20250905_usuario_ejemplo_2717ffa3b95c4679a2cf159215b99238', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (24, 'fondo_06-300x250.jpg', '20250905_usuario_ejemplo_d379daa11b26424488e52cb81ca7bb4e.jpg', '20250905_usuario_ejemplo_d379daa11b26424488e52cb81ca7bb4e', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (3, 'fondo_05-250x250.jpg', '20250903_usuario_ejemplo_ddad958fae7c4aefb7c2181b310e7fd5.jpg', '20250903_usuario_ejemplo_ddad958fae7c4aefb7c2181b310e7fd5', 'logos', 'jpg', '2025-09-03 16:33:06', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (21, 'fondo_03-300x600.jpg', '20250905_usuario_ejemplo_e1b79aae419641938b783a0e7b696eaa.jpg', '20250905_usuario_ejemplo_e1b79aae419641938b783a0e7b696eaa', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (2, 'fondo_04-250x250.jpg', '20250903_usuario_ejemplo_5233efcffa6a47c9adc2f27a85422250.jpg', '20250903_usuario_ejemplo_5233efcffa6a47c9adc2f27a85422250', 'logos', 'jpg', '2025-09-03 00:00:00', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (1, 'fondo_04-300x250.jpg', '20250903_usuario_ejemplo_0b8ea0e90e4c43bf9df8e9d298b79ab6.jpg', '20250903_usuario_ejemplo_0b8ea0e90e4c43bf9df8e9d298b79ab6', 'logos', 'jpg', '2025-09-03 00:00:00', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (22, 'fondo_06-300x600.jpg', '20250905_usuario_ejemplo_ae33ab7db43f48ea8b66403952ccbcc9.jpg', '20250905_usuario_ejemplo_ae33ab7db43f48ea8b66403952ccbcc9', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (26, 'fondo_03-300x250.jpg', '20250905_usuario_ejemplo_b8c78744c1ba4320966b744f13120758.jpg', '20250905_usuario_ejemplo_b8c78744c1ba4320966b744f13120758', 'logos', 'jpg', '2025-09-05 16:51:26', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (20, 'fondo_06-300x600.jpg', '20250905_usuario_ejemplo_7a19f06869c04bac8b0b685365c8f1c7.jpg', '20250905_usuario_ejemplo_7a19f06869c04bac8b0b685365c8f1c7', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (48, 'Boton-pagos-pse.png', '20250917_usuario_ejemplo_633558e0530f4bff8896dae6b9c8afa1.png', '20250917_usuario_ejemplo_633558e0530f4bff8896dae6b9c8afa1', 'logos', 'png', '2025-09-17 15:13:14', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (27, 'fondo_04-300x250.jpg', '20250905_usuario_ejemplo_ca89fa4bc1fb4440932e4385d6eda307.jpg', '20250905_usuario_ejemplo_ca89fa4bc1fb4440932e4385d6eda307', 'logos', 'jpg', '2025-09-05 17:35:33', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (28, 'fondo_04-300x600.jpg', '20250905_usuario_ejemplo_18eee28cf2844415aeaf1d840368afca.jpg', '20250905_usuario_ejemplo_18eee28cf2844415aeaf1d840368afca', 'logos', 'jpg', '2025-09-05 17:35:33', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (47, 'fondo_03-300x250.jpg', '20250915_usuario_ejemplo_17feccf5f5d54947ab83ea3316cea2e9.jpg', '20250915_usuario_ejemplo_17feccf5f5d54947ab83ea3316cea2e9', 'logos', 'jpg', '2025-09-15 17:59:50', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (25, 'fondo_05-250x250.jpg', '20250905_usuario_ejemplo_e6edb7267b5b4e338fd033d4615f80a8.jpg', '20250905_usuario_ejemplo_e6edb7267b5b4e338fd033d4615f80a8', 'logos', 'jpg', '2025-09-05 16:19:18', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (51, 'GenIa Answer Logo.png', '20250918_usuario_ejemplo_4e904c73b9e94abd92cdb3bffe173b9d.png', '20250918_usuario_ejemplo_4e904c73b9e94abd92cdb3bffe173b9d', 'logos', 'png', '2025-09-18 15:09:15', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (52, 'Genia Search Logo.png', '20250918_usuario_ejemplo_c9ba377bd9b04383b367d688307100c5.png', '20250918_usuario_ejemplo_c9ba377bd9b04383b367d688307100c5', 'logos', 'png', '2025-09-18 15:09:19', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (53, 'GenIA Suite.png', '20250918_usuario_ejemplo_d6d6aab0e6c74d9cafd0f729ea644527.png', '20250918_usuario_ejemplo_d6d6aab0e6c74d9cafd0f729ea644527', 'logos', 'png', '2025-09-18 15:09:19', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (54, 'GenIA Text Logo Png.png', '20250918_usuario_ejemplo_7482686d9cba4eea9f7bac5f73e6bdfa.png', '20250918_usuario_ejemplo_7482686d9cba4eea9f7bac5f73e6bdfa', 'logos', 'png', '2025-09-18 15:09:19', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (55, 'GenIa Answer Logo.png', '20250918_usuario_ejemplo_0d355bb589e7486b88a5ea95d4b835f5.png', '20250918_usuario_ejemplo_0d355bb589e7486b88a5ea95d4b835f5', 'logos', 'png', '2025-09-18 15:09:20', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (56, 'Genia Search Logo.png', '20250918_usuario_ejemplo_997bd8278955459e807377dcc62e7323.png', '20250918_usuario_ejemplo_997bd8278955459e807377dcc62e7323', 'logos', 'png', '2025-09-18 15:09:20', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (57, 'GenIA Suite.png', '20250918_usuario_ejemplo_dcaf6fc6bc164b6db1cb6e87040d3b2c.png', '20250918_usuario_ejemplo_dcaf6fc6bc164b6db1cb6e87040d3b2c', 'logos', 'png', '2025-09-18 15:09:20', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (58, 'GenIA Text Logo Png.png', '20250918_usuario_ejemplo_5d3d1ccf1ed24242a9421458f29a350a.png', '20250918_usuario_ejemplo_5d3d1ccf1ed24242a9421458f29a350a', 'logos', 'png', '2025-09-18 15:09:21', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (59, 'GenIa Answer Logo.png', '20250918_usuario_ejemplo_a056180aeea94f2eb4738f480c7a1460.png', '20250918_usuario_ejemplo_a056180aeea94f2eb4738f480c7a1460', 'logos', 'png', '2025-09-18 15:09:21', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (60, 'Genia Search Logo.png', '20250918_usuario_ejemplo_3dcfcc935848496da34253728915e2ad.png', '20250918_usuario_ejemplo_3dcfcc935848496da34253728915e2ad', 'logos', 'png', '2025-09-18 15:09:21', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (61, 'GenIA Suite.png', '20250918_usuario_ejemplo_ac04cbebbf5d4355b8fbd614fb2eb5c1.png', '20250918_usuario_ejemplo_ac04cbebbf5d4355b8fbd614fb2eb5c1', 'logos', 'png', '2025-09-18 15:09:21', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (62, 'GenIA Text Logo Png.png', '20250918_usuario_ejemplo_76ca5952cbde41f0b37ed6d6b641bd8a.png', '20250918_usuario_ejemplo_76ca5952cbde41f0b37ed6d6b641bd8a', 'logos', 'png', '2025-09-18 15:09:22', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (65, 'fondo_04-250x250.jpg', '20251009_usuario_ejemplo_ff256d57956a45b6a3e484ac8fb04d14.jpg', '20251009_usuario_ejemplo_ff256d57956a45b6a3e484ac8fb04d14', 'logos', 'jpg', '2025-10-09 15:30:25', 1, NULL, 'UFJPAAABmc');
INSERT INTO "public"."assets" VALUES (66, 'fondo_04-300x600.jpg', '20251009_admin@csalatamcom_dcba7ab6b17248239f1f36250beb2089.jpg', '20251009_admin@csalatamcom_dcba7ab6b17248239f1f36250beb2089', 'logos', 'jpg', '2025-10-09 15:37:09', 1, NULL, 'UFJPAAABmc');
INSERT INTO "public"."assets" VALUES (67, 'fondo_04-300x600.jpg', '20251009_admin@csalatamcom_de52829186fd40f597fe0ec3939678e8.jpg', '20251009_admin@csalatamcom_de52829186fd40f597fe0ec3939678e8', 'images', 'jpg', '2025-10-09 15:43:54', 1, NULL, 'UFJPAAABmc');
INSERT INTO "public"."assets" VALUES (68, '#dc143c', '', '#dc143c', 'colors', '', '2025-10-09 15:46:28', 1, NULL, 'UFJPAAABmc');
INSERT INTO "public"."assets" VALUES (69, 'ccmeanwhile-regular.ttf', '20251009_admin@csalatamcom_5e282cfe0d954584a90453b93f4c9734.ttf', '20251009_admin@csalatamcom_5e282cfe0d954584a90453b93f4c9734', 'fonts', 'ttf', '2025-10-09 15:52:25', 1, NULL, 'UFJPAAABmc');
INSERT INTO "public"."assets" VALUES (10, 'test.pptx', '20250903_usuario_ejemplo_4b7a26b729ee46ee97b755cb79e8479d.pptx', '20250903_usuario_ejemplo_4b7a26b729ee46ee97b755cb79e8479d', 'files', 'pptx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (11, 'test.xlsx', '20250903_usuario_ejemplo_7e6be877d1ca46d49665d5a7b926ca32.xlsx', '20250903_usuario_ejemplo_7e6be877d1ca46d49665d5a7b926ca32', 'files', 'xlsx', '2025-09-03 17:36:38', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (36, 'test.docx', '20250911_usuario_ejemplo_d26f0da12ee4488caa109c28e66804c5.docx', '20250911_usuario_ejemplo_d26f0da12ee4488caa109c28e66804c5', 'files', 'docx', '2025-09-11 15:50:45', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (44, 'test.pptx', '20250915_usuario_ejemplo_eb7f91d84fee46c8ba780e02dd3ac9b0.pptx', '20250915_usuario_ejemplo_eb7f91d84fee46c8ba780e02dd3ac9b0', 'files', 'pptx', '2025-09-15 17:57:29', 0, NULL, NULL);
INSERT INTO "public"."assets" VALUES (70, 'test.docx', '20251009_admin@csalatamcom_3fa4354eaafe472a8bd19216a95ddb00.docx', '20251009_admin@csalatamcom_3fa4354eaafe472a8bd19216a95ddb00', 'files', 'docx', '2025-10-09 15:56:25', 1, NULL, 'UFJPAAABmc');

-- ----------------------------
-- Table structure for brands
-- ----------------------------
DROP TABLE IF EXISTS "public"."brands";
CREATE TABLE "public"."brands" (
  "brand_id" int4 NOT NULL DEFAULT nextval('brands_brand_id_seq'::regclass),
  "brand_name" varchar(255) COLLATE "pg_catalog"."default",
  "brand_pais" varchar(255) COLLATE "pg_catalog"."default",
  "brand_subindustria" varchar(255) COLLATE "pg_catalog"."default",
  "brand_description" varchar(255) COLLATE "pg_catalog"."default",
  "brand_estado" int4
)
;

-- ----------------------------
-- Records of brands
-- ----------------------------
INSERT INTO "public"."brands" VALUES (1, 'claro', 'peru', 'telecomunicaciones', 'Prueba cambios', 1);

-- ----------------------------
-- Table structure for colecciones
-- ----------------------------
DROP TABLE IF EXISTS "public"."colecciones";
CREATE TABLE "public"."colecciones" (
  "coleccion_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "coleccion_type" varchar(255) COLLATE "pg_catalog"."default",
  "coleccion_category" varchar(255) COLLATE "pg_catalog"."default",
  "coleccion_estado" int4,
  "tendencia_id" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of colecciones
-- ----------------------------

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS "public"."config";
CREATE TABLE "public"."config" (
  "conf_id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "conf_name" varchar(255) COLLATE "pg_catalog"."default",
  "conf_value" varchar(255) COLLATE "pg_catalog"."default",
  "conf_symbol" varchar(255) COLLATE "pg_catalog"."default",
  "conf_type" varchar(255) COLLATE "pg_catalog"."default",
  "conf_estado" int4
)
;

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO "public"."config" VALUES (3, 'peru', 'peru', NULL, 'brand_pais', 1);
INSERT INTO "public"."config" VALUES (8, 'telecomunicaciones', 'telecomunicaciones', NULL, 'brand_industria', 1);
INSERT INTO "public"."config" VALUES (9, 'software', 'software', NULL, 'brand_industria', 1);
INSERT INTO "public"."config" VALUES (10, 'medios_entretenimiento', 'medios y entretenimiento
', NULL, 'brand_industria', 1);
INSERT INTO "public"."config" VALUES (11, 'admin', 'admin', NULL, 'user_permiso', 1);
INSERT INTO "public"."config" VALUES (13, 'user', 'usuario', NULL, 'user_permiso', 1);
INSERT INTO "public"."config" VALUES (14, 'client', 'cliente', NULL, 'user_permiso', 0);
INSERT INTO "public"."config" VALUES (12, 'superadmin', 'superadmin', NULL, 'user_permiso', 0);
INSERT INTO "public"."config" VALUES (1, 'colombia', 'colombia', NULL, 'brand_pais', 0);
INSERT INTO "public"."config" VALUES (2, 'ecuador', 'ecuador', NULL, 'brand_pais', 0);
INSERT INTO "public"."config" VALUES (4, 'bolivia', 'bolivia', NULL, 'brand_pais', 0);
INSERT INTO "public"."config" VALUES (5, 'mexico', 'mexico', NULL, 'brand_pais', 0);
INSERT INTO "public"."config" VALUES (6, 'chile', 'chile', NULL, 'brand_pais', 0);
INSERT INTO "public"."config" VALUES (7, 'argentina', 'argentina', NULL, 'brand_pais', 0);

-- ----------------------------
-- Table structure for exclusiones
-- ----------------------------
DROP TABLE IF EXISTS "public"."exclusiones";
CREATE TABLE "public"."exclusiones" (
  "exsite_id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "exsite_url" varchar(255) COLLATE "pg_catalog"."default",
  "exsite_fecha" timestamp(6),
  "exsite_estado" int4
)
;

-- ----------------------------
-- Records of exclusiones
-- ----------------------------

-- ----------------------------
-- Table structure for keywords
-- ----------------------------
DROP TABLE IF EXISTS "public"."keywords";
CREATE TABLE "public"."keywords" (
  "keyword_id" varchar(255) COLLATE "pg_catalog"."default",
  "keyword_name" varchar(255) COLLATE "pg_catalog"."default",
  "keyword_estado" int4,
  "keyword_metrica_name" varchar(255) COLLATE "pg_catalog"."default",
  "keyword_metrica_value" int4,
  "keyword_indicador_name" varchar(255) COLLATE "pg_catalog"."default",
  "keyword_indicador_value" int4,
  "keyword_fuente" varchar(255) COLLATE "pg_catalog"."default",
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of keywords
-- ----------------------------
INSERT INTO "public"."keywords" VALUES ('KEYi5xnFjT', 'como saber cuantas lineas tengo a mi nombre', 1, 'impresiones', 617, 'posicion', 10, 'google search', 'PROUBJOxpr');
INSERT INTO "public"."keywords" VALUES ('KEY97f01x5', 'que es roaming de datos', 1, 'impresiones', 1846, 'posicion', 10, 'google search', 'PROUBJOxpr');
INSERT INTO "public"."keywords" VALUES ('KEYzhIvZ69', 'claro sim', 1, 'N/A', 0, 'N/A', 0, 'custom', 'PROUBJOxpr');
INSERT INTO "public"."keywords" VALUES ('KEYBbjGP8m', 'television por cable', 1, 'volumen', 260, 'posicion', 5, 'semrush', 'PROUBJOxpr');

-- ----------------------------
-- Table structure for links
-- ----------------------------
DROP TABLE IF EXISTS "public"."links";
CREATE TABLE "public"."links" (
  "link_id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "link_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "link_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "link_estado" int4,
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of links
-- ----------------------------
INSERT INTO "public"."links" VALUES (2, 'el comercio', 'https://elcomercio.pe/publirreportaje/conoce-al-unico-operador-de-tv-paga-que-sigue-creciendo-en-el-peru-noticia/', 1, 'UFJPAAABmc');
INSERT INTO "public"."links" VALUES (3, 'el comercio v1', 'https://elcomercio.pe/economia/peru/osiptel-peru-supera-los-437-millones-de-lineas-moviles-y-alcanza-su-pico-historico-l-osiptel-l-ultimas-noticia/', 1, 'UFJPAAABmc');

-- ----------------------------
-- Table structure for protectos_details
-- ----------------------------
DROP TABLE IF EXISTS "public"."protectos_details";
CREATE TABLE "public"."protectos_details" (
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default",
  "asset_id" int4
)
;

-- ----------------------------
-- Records of protectos_details
-- ----------------------------

-- ----------------------------
-- Table structure for proyectos
-- ----------------------------
DROP TABLE IF EXISTS "public"."proyectos";
CREATE TABLE "public"."proyectos" (
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "proyecto_name" varchar(255) COLLATE "pg_catalog"."default",
  "proyecto_estado" int4,
  "proyecto_description" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of proyectos
-- ----------------------------
INSERT INTO "public"."proyectos" VALUES ('PROVHUAHiq', 'test', 0, 'new');
INSERT INTO "public"."proyectos" VALUES ('UFJPAAABmc', 'inter test v1', 1, 'test');
INSERT INTO "public"."proyectos" VALUES ('PROUBJOxpr', 'new planes v2', 1, 'test');

-- ----------------------------
-- Table structure for sitemap
-- ----------------------------
DROP TABLE IF EXISTS "public"."sitemap";
CREATE TABLE "public"."sitemap" (
  "site_id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "site_name" varchar(255) COLLATE "pg_catalog"."default",
  "site_url" varchar(255) COLLATE "pg_catalog"."default",
  "site_fecha" timestamp(6),
  "site_estado" int4
)
;

-- ----------------------------
-- Records of sitemap
-- ----------------------------
INSERT INTO "public"."sitemap" VALUES (13779, '', 'https://www.claro.com.pe/personas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13780, '', 'https://www.claro.com.pe/personas/sorteos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13781, '', 'https://www.claro.com.pe/personas/sorteos/ganadores/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13782, '', 'https://www.claro.com.pe/personas/movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13783, '', 'https://www.claro.com.pe/personas/movil/bases-dilesi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13784, '', 'https://www.claro.com.pe/personas/movil/activa-chip/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13785, '', 'https://www.claro.com.pe/personas/movil/conexion-smart/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13786, '', 'https://www.claro.com.pe/personas/movil/apple-watch/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13787, '', 'https://www.claro.com.pe/personas/movil/esim/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13788, '', 'https://www.claro.com.pe/personas/movil/postpago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13789, '', 'https://www.claro.com.pe/personas/movil/postpago/plan-35-90/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13790, '', 'https://www.claro.com.pe/personas/movil/postpago/ganadores-adammo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13791, '', 'https://www.claro.com.pe/personas/movil/postpago/nuevo-postpago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13792, '', 'https://www.claro.com.pe/personas/movil/postpago/planesmaxvip/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13793, '', 'https://www.claro.com.pe/personas/movil/postpago/ecocanje/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13794, '', 'https://www.claro.com.pe/personas/movil/postpago/un-buen-plan/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13795, '', 'https://www.claro.com.pe/personas/movil/postpago/planes-max/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13796, '', 'https://www.claro.com.pe/personas/movil/postpago/mas-gigas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13797, '', 'https://www.claro.com.pe/personas/movil/prepago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13798, '', 'https://www.claro.com.pe/personas/movil/prepago/diagamer/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13799, '', 'https://www.claro.com.pe/personas/movil/prepago/diagamer/bases-esbelite/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13800, '', 'https://www.claro.com.pe/personas/movil/prepago/bases-gachi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13801, '', 'https://www.claro.com.pe/personas/movil/prepago/bases-concursoredbull24/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13802, '', 'https://www.claro.com.pe/personas/movil/prepago/bases-sorteo-camisetas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13803, '', 'https://www.claro.com.pe/personas/movil/prepago/bono-inicial/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13804, '', 'https://www.claro.com.pe/personas/movil/prepago/control-automatico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13805, '', 'https://www.claro.com.pe/personas/movil/prepago/paquetes-teletrabajo-prepago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13806, '', 'https://www.claro.com.pe/personas/movil/prepago/bonos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13807, '', 'https://www.claro.com.pe/personas/movil/prepago/bono-provincia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13808, '', 'https://www.claro.com.pe/personas/movil/prepago/plan-prepagado/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13809, '', 'https://www.claro.com.pe/personas/movil/prepago/triplica-tu-recarga/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13810, '', 'https://www.claro.com.pe/personas/movil/prepago/chevere-control/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13811, '', 'https://www.claro.com.pe/personas/movil/prepago/chevere-automatico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13812, '', 'https://www.claro.com.pe/personas/movil/prepago/paquetes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13813, '', 'https://www.claro.com.pe/personas/movil/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13814, '', 'https://www.claro.com.pe/personas/movil/promociones/canje-smart/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13815, '', 'https://www.claro.com.pe/personas/movil/promociones/mas-gigas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13816, '', 'https://www.claro.com.pe/personas/movil/promociones/triple-bienvenida/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13817, '', 'https://www.claro.com.pe/personas/movil/promociones/paquetebienvenida/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13818, '', 'https://www.claro.com.pe/personas/movil/promociones/promocion-ecommerce/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13819, '', 'https://www.claro.com.pe/personas/movil/promociones/sorteo-bcp/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13820, '', 'https://www.claro.com.pe/personas/movil/recarga/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13821, '', 'https://www.claro.com.pe/personas/movil/bono-descarga-mi-claro-app/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13822, '', 'https://www.claro.com.pe/personas/movil/indecopi-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13823, '', 'https://www.claro.com.pe/personas/movil/vo-lte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13824, '', 'https://www.claro.com.pe/personas/movil/vowifi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13825, '', 'https://www.claro.com.pe/personas/movil/pack-prepago-chevere/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13826, '', 'https://www.claro.com.pe/personas/movil/bono-por-portabilidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13827, '', 'https://www.claro.com.pe/personas/movil/bono-pronto-pago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13828, '', 'https://www.claro.com.pe/personas/movil/hazla-linda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13829, '', 'https://www.claro.com.pe/personas/movil/compromiso-de-pago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13830, '', 'https://www.claro.com.pe/personas/movil/ofertas-fiestas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13831, '', 'https://www.claro.com.pe/personas/movil/combo-full/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13832, '', 'https://www.claro.com.pe/personas/movil/bases-sorteo-tonos-espera/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13833, '', 'https://www.claro.com.pe/personas/movil/dias-claro-fans/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13834, '', 'https://www.claro.com.pe/personas/movil/directorio-suscriptores/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13835, '', 'https://www.claro.com.pe/personas/movil/basesoppo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13836, '', 'https://www.claro.com.pe/personas/hogar/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13837, '', 'https://www.claro.com.pe/personas/hogar/claro-te-cuida/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13838, '', 'https://www.claro.com.pe/personas/hogar/alianzas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13839, '', 'https://www.claro.com.pe/personas/hogar/claro_aliados/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13840, '', 'https://www.claro.com.pe/personas/hogar/alianzas_educativas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13841, '', 'https://www.claro.com.pe/personas/hogar/claro-condominios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13842, '', 'https://www.claro.com.pe/personas/hogar/terminos-condiciones-oka/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13843, '', 'https://www.claro.com.pe/personas/hogar/terminos-condiciones-inst-educativas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13844, '', 'https://www.claro.com.pe/personas/hogar/sorteo-esbelite/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13845, '', 'https://www.claro.com.pe/personas/hogar/sorteo-esbelite/bases-esbelite/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13846, '', 'https://www.claro.com.pe/personas/hogar/guia-usuario/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13847, '', 'https://www.claro.com.pe/personas/hogar/internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13848, '', 'https://www.claro.com.pe/personas/hogar/internet/lima/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13849, '', 'https://www.claro.com.pe/personas/hogar/internet-app/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13850, '', 'https://www.claro.com.pe/personas/hogar/olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13851, '', 'https://www.claro.com.pe/personas/hogar/olo/recarga/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13852, '', 'https://www.claro.com.pe/personas/hogar/olo/soporte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13853, '', 'https://www.claro.com.pe/personas/hogar/olo/sorteo-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13854, '', 'https://www.claro.com.pe/personas/hogar/olo/nuevo-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13855, '', 'https://www.claro.com.pe/personas/hogar/ifi-volte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13856, '', 'https://www.claro.com.pe/personas/hogar/ifi-volte/recarga/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13857, '', 'https://www.claro.com.pe/personas/hogar/ifi-volte/soporte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13858, '', 'https://www.claro.com.pe/personas/hogar/ifi-volte/sorteo-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13859, '', 'https://www.claro.com.pe/personas/hogar/ifi-volte/nuevo-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13860, '', 'https://www.claro.com.pe/personas/hogar/plan-ideal/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13861, '', 'https://www.claro.com.pe/personas/hogar/telefono-fijo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13862, '', 'https://www.claro.com.pe/personas/hogar/tips-internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13863, '', 'https://www.claro.com.pe/personas/hogar/tv/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13864, '', 'https://www.claro.com.pe/personas/hogar/tv/canales-tv-satelital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13865, '', 'https://www.claro.com.pe/personas/hogar/tv/canales-digitales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13866, '', 'https://www.claro.com.pe/personas/hogar/tv/canales-premium/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13867, '', 'https://www.claro.com.pe/personas/hogar/tv/canales-premium/universal-plus/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13868, '', 'https://www.claro.com.pe/personas/hogar/tv/canales-premium/hbo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13869, '', 'https://www.claro.com.pe/personas/hogar/tv/guia-de-programacion/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13870, '', 'https://www.claro.com.pe/personas/hogar/tv/nueva-claro-tv/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13871, '', 'https://www.claro.com.pe/personas/hogar/tv/claro-tv-flex/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13872, '', 'https://www.claro.com.pe/personas/hogar/tv/claro-tv-mas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13873, '', 'https://www.claro.com.pe/personas/hogar/actualizacion-router/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13874, '', 'https://www.claro.com.pe/personas/hogar/planes-teletrabajo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13875, '', 'https://www.claro.com.pe/personas/hogar/playas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13876, '', 'https://www.claro.com.pe/personas/hogar/internet-lte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13877, '', 'https://www.claro.com.pe/personas/hogar/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13878, '', 'https://www.claro.com.pe/personas/hogar/promociones/promocion-inalambrica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13879, '', 'https://www.claro.com.pe/personas/hogar/promociones/promocion-tv-sat/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13880, '', 'https://www.claro.com.pe/personas/hogar/promociones/promocion-inalambrica-app/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13881, '', 'https://www.claro.com.pe/personas/hogar/planes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13882, '', 'https://www.claro.com.pe/personas/hogar/tarifa-acceso/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13883, '', 'https://www.claro.com.pe/personas/hogar/oferta-fija/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13884, '', 'https://www.claro.com.pe/personas/hogar/oferta-fija-experience/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13885, '', 'https://www.claro.com.pe/personas/hogar/oferta-provincia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13886, '', 'https://www.claro.com.pe/personas/hogar/oferta-samsung-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13887, '', 'https://www.claro.com.pe/personas/hogar/ganadores-claro-musica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13888, '', 'https://www.claro.com.pe/personas/hogar/internet-inalambrico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13889, '', 'https://www.claro.com.pe/personas/hogar/olo15/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13890, '', 'https://www.claro.com.pe/personas/hogar/upsell/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13891, '', 'https://www.claro.com.pe/personas/hogar/forms/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13892, '', 'https://www.claro.com.pe/personas/hogar/embajadores/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13893, '', 'https://www.claro.com.pe/personas/hogar/referidos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13894, '', 'https://www.claro.com.pe/personas/hogar/paquetes-ifi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13895, '', 'https://www.claro.com.pe/personas/hogar/soft-carrito/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13896, '', 'https://www.claro.com.pe/personas/app/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13897, '', 'https://www.claro.com.pe/personas/app/claro-musica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13898, '', 'https://www.claro.com.pe/personas/app/claro-musica/sorteo-redbull/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13899, '', 'https://www.claro.com.pe/personas/app/claro-club/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13900, '', 'https://www.claro.com.pe/personas/app/claro-drive/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13901, '', 'https://www.claro.com.pe/personas/app/claro-video/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13902, '', 'https://www.claro.com.pe/personas/app/claro-video/movie-snack/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13903, '', 'https://www.claro.com.pe/personas/app/claro-video/diadecine/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13904, '', 'https://www.claro.com.pe/personas/app/claro-video_bck/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13905, '', 'https://www.claro.com.pe/personas/app/claro-video_bck/movie-snack/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13906, '', 'https://www.claro.com.pe/personas/app/claro-video_bck/diadecine/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13907, '', 'https://www.claro.com.pe/personas/app/mi-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13908, '', 'https://www.claro.com.pe/personas/app/mi-claro/contrasena-unica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13909, '', 'https://www.claro.com.pe/personas/app/smart-home/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13910, '', 'https://www.claro.com.pe/personas/beneficios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13911, '', 'https://www.claro.com.pe/personas/beneficios/antisubasta/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13912, '', 'https://www.claro.com.pe/personas/beneficios/claro-club/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13913, '', 'https://www.claro.com.pe/personas/beneficios/claro-club/millas-latam-pass/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13914, '', 'https://www.claro.com.pe/personas/beneficios/claro-club/podcast/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13915, '', 'https://www.claro.com.pe/personas/beneficios/claro-club/canje-claro-puntos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13916, '', 'https://www.claro.com.pe/personas/beneficios/claro-club/sorteo-entradas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13917, '', 'https://www.claro.com.pe/personas/beneficios/full-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13918, '', 'https://www.claro.com.pe/personas/beneficios/hogar/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13919, '', 'https://www.claro.com.pe/personas/beneficios/hogar/extensores-wifi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13920, '', 'https://www.claro.com.pe/personas/beneficios/hogar/wifi-360-plume/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13921, '', 'https://www.claro.com.pe/personas/beneficios/hogar/extensores-wifi-v2/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13922, '', 'https://www.claro.com.pe/personas/beneficios/hogar/hot-go/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13923, '', 'https://www.claro.com.pe/personas/beneficios/hogar/recupera-tu-velocidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13924, '', 'https://www.claro.com.pe/personas/beneficios/hogar/sorteo-warnerbros-discovery/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13925, '', 'https://www.claro.com.pe/personas/beneficios/hogar/antivirus-panda-security/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13926, '', 'https://www.claro.com.pe/personas/beneficios/hogar/sorteo-huawei/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13927, '', 'https://www.claro.com.pe/personas/beneficios/movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13928, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-oppo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13929, '', 'https://www.claro.com.pe/personas/beneficios/movil/rescatel/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13930, '', 'https://www.claro.com.pe/personas/beneficios/movil/app-touch/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13931, '', 'https://www.claro.com.pe/personas/beneficios/movil/busuu/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13932, '', 'https://www.claro.com.pe/personas/beneficios/movil/claro-juegos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13933, '', 'https://www.claro.com.pe/personas/beneficios/movil/club-claro-apps/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13934, '', 'https://www.claro.com.pe/personas/beneficios/movil/cobertura-internacional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13935, '', 'https://www.claro.com.pe/personas/beneficios/movil/cobertura-internacional-prepago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13936, '', 'https://www.claro.com.pe/personas/beneficios/movil/fbpaquetes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13937, '', 'https://www.claro.com.pe/personas/beneficios/movil/google-play/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13938, '', 'https://www.claro.com.pe/personas/beneficios/movil/habla-ilimitado-a-cualquier-operador/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13939, '', 'https://www.claro.com.pe/personas/beneficios/movil/huawei-carrier-billing/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13940, '', 'https://www.claro.com.pe/personas/beneficios/movil/limite-de-consumo-adicional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13941, '', 'https://www.claro.com.pe/personas/beneficios/movil/limite-de-consumo-exacto/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13942, '', 'https://www.claro.com.pe/personas/beneficios/movil/lineas-adicionales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13943, '', 'https://www.claro.com.pe/personas/beneficios/movil/llamada-por-cobrar/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13944, '', 'https://www.claro.com.pe/personas/beneficios/movil/minutos-todo-destino/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13945, '', 'https://www.claro.com.pe/personas/beneficios/movil/norton-family/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13946, '', 'https://www.claro.com.pe/personas/beneficios/movil/norton-security/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13947, '', 'https://www.claro.com.pe/personas/beneficios/movil/norton-vpn/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13948, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquete-internacional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13949, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquetes-internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13950, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquetes-sms/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13951, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquetes-teletrabajo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13952, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquetes-cobertura-internacional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13953, '', 'https://www.claro.com.pe/personas/beneficios/movil/portal-claro-ideas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13954, '', 'https://www.claro.com.pe/personas/beneficios/movil/prestame-saldo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13955, '', 'https://www.claro.com.pe/personas/beneficios/movil/proteccion-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13956, '', 'https://www.claro.com.pe/personas/beneficios/movil/respaldo-agenda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13957, '', 'https://www.claro.com.pe/personas/beneficios/movil/solicita-saldo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13958, '', 'https://www.claro.com.pe/personas/beneficios/movil/tonos-de-espera/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13959, '', 'https://www.claro.com.pe/personas/beneficios/movil/pasa-saldo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13960, '', 'https://www.claro.com.pe/personas/beneficios/movil/whatsapp-gratis/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13961, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-bcp-huawei/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13962, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-bcp-1000-soles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13963, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-fiestas-patrias/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13964, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-zte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13965, '', 'https://www.claro.com.pe/personas/beneficios/movil/promo-chip-prepago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13966, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-dia-padre/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13967, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-dia-madre/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13968, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-celulares/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13969, '', 'https://www.claro.com.pe/personas/beneficios/movil/paquetes-tiktok/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13970, '', 'https://www.claro.com.pe/personas/beneficios/movil/carrier-billing/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13971, '', 'https://www.claro.com.pe/personas/beneficios/movil/equipo-vale-plata/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13972, '', 'https://www.claro.com.pe/personas/beneficios/movil/mas-megas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13973, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-concierto-jaze/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13974, '', 'https://www.claro.com.pe/personas/beneficios/movil/sorteo-redbull-fonoboleto/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13975, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-pago-digital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13976, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-pronto-pago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13977, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-recibo-vencido/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13978, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-bono-gb/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13979, '', 'https://www.claro.com.pe/personas/beneficios/actualiza-tu-correo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13980, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-debito-automatico-interbank/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13981, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-pago-automatico-bcp/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13982, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-pago-yape/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13983, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-canales-digitales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13984, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-vales-consumo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13985, '', 'https://www.claro.com.pe/personas/beneficios/beneficios-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13986, '', 'https://www.claro.com.pe/personas/beneficios/oferta-fullclaro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13987, '', 'https://www.claro.com.pe/personas/beneficios/full-claro-comparte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13988, '', 'https://www.claro.com.pe/personas/beneficios/simulador-fullclaro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13989, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-samsung/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13990, '', 'https://www.claro.com.pe/personas/beneficios/sorteo-pura-calle/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13991, '', 'https://www.claro.com.pe/personas/beneficios/vacunateya/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13992, '', 'https://www.claro.com.pe/personas/activa-tu-plan-netflix/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13993, '', 'https://www.claro.com.pe/personas/activa-tu-plan-netflix/activacion-netflix/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13994, '', 'https://www.claro.com.pe/personas/tienda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13995, '', 'https://www.claro.com.pe/personas/tienda/celulares/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13996, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13997, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/galaxy-s23/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13998, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/galaxy-s24/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (13999, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/galaxy-s25/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14000, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/iphone-14/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14001, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/galaxy_z_fold_5_y_z_flip_5/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14002, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/iphone-15/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14003, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/iphone-16/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14004, '', 'https://www.claro.com.pe/personas/tienda/nuevos-lanzamientos/iphone-17/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14005, '', 'https://www.claro.com.pe/personas/estamos-juntos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14006, '', 'https://www.claro.com.pe/personas/estamos-juntos/servicio-de-emergencia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14007, '', 'https://www.claro.com.pe/personas/estamos-juntos/protocolo-delivery/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14008, '', 'https://www.claro.com.pe/personas/componentes-hogar-beneficios-fullclaro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14009, '', 'https://www.claro.com.pe/personas/agenda-tu-cita/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14010, '', 'https://www.claro.com.pe/personas/sorteo-fiestas-patrias/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14011, '', 'https://www.claro.com.pe/personas/consideraciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14012, '', 'https://www.claro.com.pe/personas/centro-de-ayuda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14013, '', 'https://www.claro.com.pe/personas/centro-de-ayuda/te-escuchamos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14014, '', 'https://www.claro.com.pe/personas/navidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14015, '', 'https://www.claro.com.pe/personas/conoce-tu-recibo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14016, '', 'https://www.claro.com.pe/personas/conoce-tu-recibo/debito-automatico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14017, '', 'https://www.claro.com.pe/personas/olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14018, '', 'https://www.claro.com.pe/personas/olo/que-es-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14019, '', 'https://www.claro.com.pe/personas/olo/recarga-paquetes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14020, '', 'https://www.claro.com.pe/personas/olo/cobertura/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14021, '', 'https://www.claro.com.pe/personas/olo/login-mi-olo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14022, '', 'https://www.claro.com.pe/personas/olo/accesibilidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14023, '', 'https://www.claro.com.pe/personas/olo/libro-de-reclamaciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14024, '', 'https://www.claro.com.pe/personas/olo/indicadores-de-calidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14025, '', 'https://www.claro.com.pe/personas/olo/informacion-abonados-y-usuarios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14026, '', 'https://www.claro.com.pe/personas/olo/comprobantes-electronicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14027, '', 'https://www.claro.com.pe/personas/olo/terminos-y-condiciones-routers/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14028, '', 'https://www.claro.com.pe/personas/olo/internet-portatil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14029, '', 'https://www.claro.com.pe/personas/olo/centro-ayuda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14030, '', 'https://www.claro.com.pe/personas/olo/centro-ayuda/reset-router/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14031, '', 'https://www.claro.com.pe/personas/olo/centro-ayuda/cambio-de-clave/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14032, '', 'https://www.claro.com.pe/empresas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14033, '', 'https://www.claro.com.pe/empresas/fijos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14034, '', 'https://www.claro.com.pe/empresas/fijos/internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14035, '', 'https://www.claro.com.pe/empresas/fijos/internet/internet-corporativo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14036, '', 'https://www.claro.com.pe/empresas/fijos/internet/internet-vsat/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14037, '', 'https://www.claro.com.pe/empresas/fijos/internet/internet-seguro-perumin/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14038, '', 'https://www.claro.com.pe/empresas/fijos/red/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14039, '', 'https://www.claro.com.pe/empresas/fijos/red/carrier-ethernet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14040, '', 'https://www.claro.com.pe/empresas/fijos/red/enlaces-satelitales-vsat/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14041, '', 'https://www.claro.com.pe/empresas/fijos/red/red-claro-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14042, '', 'https://www.claro.com.pe/empresas/fijos/red/red-privada-virtual/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14043, '', 'https://www.claro.com.pe/empresas/fijos/red/red-privada-virtual-internacional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14044, '', 'https://www.claro.com.pe/empresas/fijos/telefonia-fija/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14045, '', 'https://www.claro.com.pe/empresas/fijos/telefonia-fija/servicio-0800/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14046, '', 'https://www.claro.com.pe/empresas/fijos/telefonia-fija/telefonia-analogica-corporativa/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14047, '', 'https://www.claro.com.pe/empresas/fijos/telefonia-fija/telefonia-fija-e1-pri/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14048, '', 'https://www.claro.com.pe/empresas/fijos/telefonia-fija/telefonia-troncal-sip/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14049, '', 'https://www.claro.com.pe/empresas/fijos/tv/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14050, '', 'https://www.claro.com.pe/empresas/fijos/tv-satelital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14051, '', 'https://www.claro.com.pe/empresas/movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14052, '', 'https://www.claro.com.pe/empresas/movil/planes-conectividad-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14053, '', 'https://www.claro.com.pe/empresas/movil/planes-conectividad-movil/comparador/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14054, '', 'https://www.claro.com.pe/empresas/movil/telefonia-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14055, '', 'https://www.claro.com.pe/empresas/movil/telefonia-movil/plan/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14056, '', 'https://www.claro.com.pe/empresas/movil/telefonia-movil/bolsas-de-voz/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14057, '', 'https://www.claro.com.pe/empresas/movil/telefonia-movil/recargas_old/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14058, '', 'https://www.claro.com.pe/empresas/movil/telefonia-movil/recargas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14059, '', 'https://www.claro.com.pe/empresas/movil/internet-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14060, '', 'https://www.claro.com.pe/empresas/movil/volte-vowifi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14061, '', 'https://www.claro.com.pe/empresas/movil/dual-connect/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14062, '', 'https://www.claro.com.pe/empresas/movil/iPhone14/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14063, '', 'https://www.claro.com.pe/empresas/evento/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14064, '', 'https://www.claro.com.pe/empresas/evento/perumin/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14065, '', 'https://www.claro.com.pe/empresas/evento/perumin/ddos-summit-peru/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14066, '', 'https://www.claro.com.pe/empresas/evento/perumin-37/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14067, '', 'https://www.claro.com.pe/empresas/evento/perumin-37/radware/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14068, '', 'https://www.claro.com.pe/empresas/evento/perumin-37/fortinet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14069, '', 'https://www.claro.com.pe/empresas/evento/perumin-37/cisco/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14070, '', 'https://www.claro.com.pe/empresas/evento/tech-nights/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14071, '', 'https://www.claro.com.pe/empresas/evento/tech-nights-norte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14072, '', 'https://www.claro.com.pe/empresas/evento/webinar/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14073, '', 'https://www.claro.com.pe/empresas/evento/seguridad-sse/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14074, '', 'https://www.claro.com.pe/empresas/evento/lima-cloudshift/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14075, '', 'https://www.claro.com.pe/empresas/evento/hughes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14076, '', 'https://www.claro.com.pe/empresas/soluciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14077, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14078, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/siem-intelligence/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14079, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/anti-ddos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14080, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/sase/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14081, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/correo-seguro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14082, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/seguridad-administrada/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14083, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/seguridad-administrada-virtual/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14084, '', 'https://www.claro.com.pe/empresas/soluciones/ciberseguridad/seguridad-sse/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14085, '', 'https://www.claro.com.pe/empresas/soluciones/data-center/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14086, '', 'https://www.claro.com.pe/empresas/soluciones/data-center/nube-privada-hosteada/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14087, '', 'https://www.claro.com.pe/empresas/soluciones/data-center/colocacion/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14088, '', 'https://www.claro.com.pe/empresas/soluciones/data-center/copia-de-seguridad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14089, '', 'https://www.claro.com.pe/empresas/soluciones/data-center/almacenamiento-a-gran-escala/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14090, '', 'https://www.claro.com.pe/empresas/soluciones/cloud/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14091, '', 'https://www.claro.com.pe/empresas/soluciones/cloud/factura-electronica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14092, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14093, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/balanceo-de-enlaces/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14094, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/gestion-de-aplicaciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14095, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/lan-gestionada/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14096, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/pbx-gestionada/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14097, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/SD-WAN/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14098, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/seguridad-edr/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14099, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/rastreo-dark-web/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14100, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/inteligencia-de-amenazas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14101, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/wifi-gestionado/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14102, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/seguridad-mdr/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14103, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/gestion-de-aplicaciones-virtual/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14104, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/ciberinteligencia-de-amenazas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14105, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/comunicaciones-unificadas-cisco/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14106, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/clarocontact/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14107, '', 'https://www.claro.com.pe/empresas/soluciones/servicios-gestionados/wifi-pro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14108, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14109, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-message/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14110, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/adm-de-dispositivos-moviles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14111, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-activity/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14112, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-contact/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14113, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-content/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14114, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-delivery/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14115, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-mobility/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14116, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-presence/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14117, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-sales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14118, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-security/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14119, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-track/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14120, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/e-visit/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14121, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/formularios-dinamicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14122, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/gestion-financiera/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14123, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/localizacion-vehicular/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14124, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/mensajeria-corporativa/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14125, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/monitoreo-y-gestion-a-distancia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14126, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-moviles/smart-distancing/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14127, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14128, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/chatbot/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14129, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/estacion-remota-segura/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14130, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/portal-web/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14131, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/rpa/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14132, '', 'https://www.claro.com.pe/empresas/soluciones/soluciones-ti/mesa-de-ayuda/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14133, '', 'https://www.claro.com.pe/empresas/produce/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14134, '', 'https://www.claro.com.pe/empresas/boletin-ciberseguridad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14135, '', 'https://www.claro.com.pe/empresas/boletin-ciberseguridad/cancelar-suscripcion/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14136, '', 'https://www.claro.com.pe/negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14137, '', 'https://www.claro.com.pe/negocios/movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14138, '', 'https://www.claro.com.pe/negocios/movil/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14139, '', 'https://www.claro.com.pe/negocios/movil/promociones/duplica-tus-gigas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14140, '', 'https://www.claro.com.pe/negocios/movil/promociones/correo-ilimitado-gratis/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14141, '', 'https://www.claro.com.pe/negocios/movil/oferta-max-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14142, '', 'https://www.claro.com.pe/negocios/movil/volte-vowifi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14143, '', 'https://www.claro.com.pe/negocios/movil/telefonia-movil-p/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14144, '', 'https://www.claro.com.pe/negocios/beneficios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14145, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14146, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/bolsas-de-minutos-multidestino/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14147, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/central-fisica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14148, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/central-virtual/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14149, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/conectividad-pos-ip/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14150, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/direccion-ip/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14151, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/hunting/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14152, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/lineas-adicionales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14153, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14154, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/internet/fibra-optica-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14155, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/internet/oferta-fibra-optica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14156, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/wi-fi-inteligente/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14157, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14158, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/promociones/servicios-fijos-inalambricos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14159, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/oferta-empresas-digital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14160, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/oferta-empresas-digital/herramientas-digitales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14161, '', 'https://www.claro.com.pe/negocios/beneficios/fijos/oferta-fija/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14162, '', 'https://www.claro.com.pe/negocios/beneficios/fullclaro-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14163, '', 'https://www.claro.com.pe/negocios/beneficios/movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14164, '', 'https://www.claro.com.pe/negocios/beneficios/movil/claro-emprendedor/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14165, '', 'https://www.claro.com.pe/negocios/beneficios/movil/cobertura-internacional-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14166, '', 'https://www.claro.com.pe/negocios/beneficios/movil/minutos-premium/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14167, '', 'https://www.claro.com.pe/negocios/beneficios/movil/norton-security/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14168, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-datos-cobertura-internacional/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14169, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14170, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-minutos-cdi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14171, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-minutos-internacionales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14172, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-minutos-llama-nomas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14173, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-redes-sociales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14174, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-gb-plus/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14175, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-teletrabajo-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14176, '', 'https://www.claro.com.pe/negocios/beneficios/movil/red-privada-claro-rpc/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14177, '', 'https://www.claro.com.pe/negocios/beneficios/movil/rpc-plus/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14178, '', 'https://www.claro.com.pe/negocios/beneficios/movil/oferta-max-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14179, '', 'https://www.claro.com.pe/negocios/beneficios/movil/planes-conectividad-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14180, '', 'https://www.claro.com.pe/negocios/beneficios/movil/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14181, '', 'https://www.claro.com.pe/negocios/beneficios/movil/promociones/duplica-tus-gigas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14182, '', 'https://www.claro.com.pe/negocios/beneficios/movil/promociones/facebook-gratis/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14183, '', 'https://www.claro.com.pe/negocios/beneficios/movil/promociones/whatsapp-gratis-para-todos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14184, '', 'https://www.claro.com.pe/negocios/beneficios/movil/telefonia-movi/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14185, '', 'https://www.claro.com.pe/negocios/beneficios/movil/telefonia-movil/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14186, '', 'https://www.claro.com.pe/negocios/beneficios/movil/paquetes-de-sms/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14187, '', 'https://www.claro.com.pe/negocios/beneficios/simulador-fullclaro-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14188, '', 'https://www.claro.com.pe/negocios/distribuidores/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14189, '', 'https://www.claro.com.pe/negocios/contrata-con-ruc/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14190, '', 'https://www.claro.com.pe/negocios/kits-teletrabajo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14191, '', 'https://www.claro.com.pe/negocios/soluciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14192, '', 'https://www.claro.com.pe/negocios/soluciones/emprende-tu-idea/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14193, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14194, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/oferta-e-track/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14195, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/oferta-e-contact/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14196, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/adm-de-dispositivos-moviles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14197, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-activity/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14198, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-contact/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14199, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-content/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14200, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-delivery/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14201, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-message/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14202, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-mobility/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14203, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-presence/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14204, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-sales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14205, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-security/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14206, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-track/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14207, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-card/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14208, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/e-visit/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14209, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/formularios-dinamicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14210, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/gestion-financiera/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14211, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/localizador-vehicular/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14212, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/mensajeria-corporativa/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14213, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/monitoreo-y-gestion-a-distancia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14214, '', 'https://www.claro.com.pe/negocios/soluciones/soluciones-moviles/smart-distancing/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14215, '', 'https://www.claro.com.pe/negocios/soluciones/cloud/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14216, '', 'https://www.claro.com.pe/negocios/soluciones/cloud/factura-electronica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14217, '', 'https://www.claro.com.pe/negocios/soluciones/cloud-correo-empresas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14218, '', 'https://www.claro.com.pe/negocios/soluciones/cloud-tienda-virtual/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14219, '', 'https://www.claro.com.pe/negocios/soluciones/cloud-claro-backup/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14220, '', 'https://www.claro.com.pe/negocios/soluciones/servicios-gestionados/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14221, '', 'https://www.claro.com.pe/negocios/soluciones/oferta-e-sales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14222, '', 'https://www.claro.com.pe/negocios/soluciones/teletrabajo-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14223, '', 'https://www.claro.com.pe/negocios/fijos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14224, '', 'https://www.claro.com.pe/negocios/fijos/internet-p/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14225, '', 'https://www.claro.com.pe/negocios/fijos/internet/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14226, '', 'https://www.claro.com.pe/negocios/fijos/internet/oferta-fibra-optica/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14227, '', 'https://www.claro.com.pe/negocios/fijos/internet/internet-empresas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14228, '', 'https://www.claro.com.pe/negocios/fijos/internet/internet-fijo-inalambrico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14229, '', 'https://www.claro.com.pe/negocios/fijos/internet/lte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14230, '', 'https://www.claro.com.pe/negocios/fijos/internet/fibra-optica-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14231, '', 'https://www.claro.com.pe/negocios/fijos/internet/tecnologia-hfc-negocios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14232, '', 'https://www.claro.com.pe/negocios/fijos/promociones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14233, '', 'https://www.claro.com.pe/negocios/fijos/promociones/servicios-fijos-inalambricos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14234, '', 'https://www.claro.com.pe/negocios/fijos/oferta-empresas-digital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14235, '', 'https://www.claro.com.pe/negocios/fijos/oferta-empresas-digital/herramientas-digitales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14236, '', 'https://www.claro.com.pe/negocios/fijos/oferta-fija/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14237, '', 'https://www.claro.com.pe/negocios/fijos/juntos-impulsamos-tu-negocio/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14238, '', 'https://www.claro.com.pe/negocios/fijos/paquetizados/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14239, '', 'https://www.claro.com.pe/negocios/fijos/planes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14240, '', 'https://www.claro.com.pe/negocios/fijos/planes/comparador/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14241, '', 'https://www.claro.com.pe/deportes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14242, '', 'https://www.claro.com.pe/deportes/juegos-olimpicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14243, '', 'https://www.claro.com.pe/deportes/futbol/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14244, '', 'https://www.claro.com.pe/deportes/futbol/torneo-mas-grande-de-america/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14245, '', 'https://www.claro.com.pe/deportes/futbol/torneo-mas-grande-de-america/bases-sorteo-camisetas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14246, '', 'https://www.claro.com.pe/deportes/futbol/eliminatorias/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14247, '', 'https://www.claro.com.pe/deportes/futbol/eliminatorias/bases-sorteo-camisetas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14248, '', 'https://www.claro.com.pe/deportes/futbol/liga-1/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14249, '', 'https://www.claro.com.pe/deportes/futbol/liga-1/bases-sorteo-camisetas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14250, '', 'https://www.claro.com.pe/deportes/futbol/liga-2/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14251, '', 'https://www.claro.com.pe/deportes/juegos-paralimpicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14252, '', 'https://www.claro.com.pe/conoce-tu-recibo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14253, '', 'https://www.claro.com.pe/conoce-tu-recibo/canales-digitales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14254, '', 'https://www.claro.com.pe/conoce-tu-recibo/debito-automatico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14255, '', 'https://www.claro.com.pe/conoce-tu-recibo/debito-automatico/bbva/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14256, '', 'https://www.claro.com.pe/conoce-tu-recibo/debito-automatico/monto-tope/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14257, '', 'https://www.claro.com.pe/conoce-tu-recibo/canales-presenciales/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14258, '', 'https://www.claro.com.pe/conoce-tu-recibo/recibo-electronico/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14259, '', 'https://www.claro.com.pe/vecinoclaro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14260, '', 'https://www.claro.com.pe/portabilidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14261, '', 'https://www.claro.com.pe/osiptel-comunicado/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14262, '', 'https://www.claro.com.pe/4g-lte/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14263, '', 'https://www.claro.com.pe/carroslocos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14264, '', 'https://www.claro.com.pe/solicitud/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14265, '', 'https://www.claro.com.pe/codigo-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14266, '', 'https://www.claro.com.pe/atencion-de-reclamos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14267, '', 'https://www.claro.com.pe/atencion-de-reclamos/haz-tu-reclamo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14268, '', 'https://www.claro.com.pe/atencion-de-reclamos/consulta-el-estado-de-tu-reclamo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14269, '', 'https://www.claro.com.pe/atencion-de-reclamos/apelaciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14270, '', 'https://www.claro.com.pe/atencion-de-reclamos/quejas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14271, '', 'https://www.claro.com.pe/atencion-de-reclamos/libro-reclamaciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14272, '', 'https://www.claro.com.pe/atencion-de-reclamos/recuperar-clave/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14273, '', 'https://www.claro.com.pe/claro-informado/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14274, '', 'https://www.claro.com.pe/clarogaming/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14275, '', 'https://www.claro.com.pe/clarogaming/sorteo-masgamer/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14276, '', 'https://www.claro.com.pe/renovacion/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14277, '', 'https://www.claro.com.pe/roaming/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14278, '', 'https://www.claro.com.pe/comprobantes-electronicos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14279, '', 'https://www.claro.com.pe/consulta-de-numero/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14280, '', 'https://www.claro.com.pe/consulta-de-reclamos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14281, '', 'https://www.claro.com.pe/contactanos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14282, '', 'https://www.claro.com.pe/contactanos/ingresa-con-tu-mascota/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14283, '', 'https://www.claro.com.pe/contactanos/ingresa-con-tu-mascota/protocolo-para-mascotas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14284, '', 'https://www.claro.com.pe/contactanos/ingresa-con-tu-mascota/guia-de-limpieza-para-mascotas/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14285, '', 'https://www.claro.com.pe/contactanos/alerta-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14286, '', 'https://www.claro.com.pe/contactanos/whatsapp-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14287, '', 'https://www.claro.com.pe/directorio-de-abonados-fijos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14288, '', 'https://www.claro.com.pe/desbloquea-tu-celular/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14289, '', 'https://www.claro.com.pe/directorio-de-abonados-moviles/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14290, '', 'https://www.claro.com.pe/gigared/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14291, '', 'https://www.claro.com.pe/5g/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14292, '', 'https://www.claro.com.pe/renteseg/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14293, '', 'https://www.claro.com.pe/traficoenvivo/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14294, '', 'https://www.claro.com.pe/legal-y-regulatorio/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14295, '', 'https://www.claro.com.pe/legal-y-regulatorio/combo-full/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14296, '', 'https://www.claro.com.pe/legal-y-regulatorio/derechos-arco/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14297, '', 'https://www.claro.com.pe/legal-y-regulatorio/contrato-de-abonados-vigentes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14298, '', 'https://www.claro.com.pe/legal-y-regulatorio/contrato-de-abonados-no-vigentes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14299, '', 'https://www.claro.com.pe/legal-y-regulatorio/devolucion-prepago/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14300, '', 'https://www.claro.com.pe/legal-y-regulatorio/devoluciones-por-interrupciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14301, '', 'https://www.claro.com.pe/informacion-a-abonados-y-usuarios/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14302, '', 'https://www.claro.com.pe/informacion-a-abonados-y-usuarios/derechos-arco/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14303, '', 'https://www.claro.com.pe/informacion-a-abonados-y-usuarios/contrato-de-abonados-vigentes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14304, '', 'https://www.claro.com.pe/informacion-a-abonados-y-usuarios/contrato-de-abonados-no-vigentes/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14305, '', 'https://www.claro.com.pe/informacion-a-abonados-y-usuarios/devoluciones-por-interrupciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14306, '', 'https://www.claro.com.pe/proteccion-datos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14307, '', 'https://www.claro.com.pe/politicas-privacidad-datos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14308, '', 'https://www.claro.com.pe/terminos-y-condiciones-de-la-web/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14309, '', 'https://www.claro.com.pe/prevencion-antifraude/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14310, '', 'https://www.claro.com.pe/llamada-internacional-1912/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14311, '', 'https://www.claro.com.pe/mide-tu-velocidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14312, '', 'https://www.claro.com.pe/mide-tu-velocidad/terminos-y-condiciones/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14313, '', 'https://www.claro.com.pe/recibo-digital/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14314, '', 'https://www.claro.com.pe/comunicacion-en-emergencia/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14315, '', 'https://www.claro.com.pe/solicitudes-en-linea/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14316, '', 'https://www.claro.com.pe/trabajos-de-mantenimiento/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14317, '', 'https://www.claro.com.pe/garantia_equipos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14318, '', 'https://www.claro.com.pe/funcionalidad-de-bloqueo-de-equipos/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14319, '', 'https://www.claro.com.pe/bicentenario/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14320, '', 'https://www.claro.com.pe/hazlorealidad/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14321, '', 'https://www.claro.com.pe/making-off/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14322, '', 'https://www.claro.com.pe/me-queda-claro/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14323, '', 'https://www.claro.com.pe/logros/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14324, '', 'https://www.claro.com.pe/formulario-cac-colaborador/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14325, '', 'https://www.claro.com.pe/socio-comercial/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14326, '', 'https://www.claro.com.pe/cobertura/', '2025-09-18 20:52:30', 1);
INSERT INTO "public"."sitemap" VALUES (14327, '', 'https://www.claro.com.pe/cobertura/centros-de-atencion/', '2025-09-18 20:52:30', 1);

-- ----------------------------
-- Table structure for tendencias
-- ----------------------------
DROP TABLE IF EXISTS "public"."tendencias";
CREATE TABLE "public"."tendencias" (
  "tendencia_id" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_name" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_estado" int4,
  "proyecto_id" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_metrica_name" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_metrica_value" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_indicador_name" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_indicadot_value" varchar(255) COLLATE "pg_catalog"."default",
  "tendencia_fuente" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of tendencias
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "user_id" int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1
),
  "user_name" varchar(255) COLLATE "pg_catalog"."default",
  "user_phone" varchar(255) COLLATE "pg_catalog"."default",
  "user_email" varchar(255) COLLATE "pg_catalog"."default",
  "user_pass" varchar(255) COLLATE "pg_catalog"."default",
  "user_permiso" varchar(255) COLLATE "pg_catalog"."default",
  "user_estado" int4
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES (3, 'superadmin', '987654321', 'superadmin@csalatam.com', '21232f297a57a5a743894a0e4a801fc3', 'superadmin', 1);
INSERT INTO "public"."users" VALUES (2, 'admin', '987654325', 'test@csalatam.com', '21232f297a57a5a743894a0e4a801fc3', 'user', 1);
INSERT INTO "public"."users" VALUES (1, 'admin claro', '987654321', 'admin@csalatam.com', '21232f297a57a5a743894a0e4a801fc3', 'admin', 1);
INSERT INTO "public"."users" VALUES (4, 'test2', '987351452', 'test2@test.com', 'e99a18c428cb38d5f260853678922e03', 'user', 1);
INSERT INTO "public"."users" VALUES (5, 'test3', '987353545', 'test3@csa.com', 'e99a18c428cb38d5f260853678922e03', 'user', 1);
INSERT INTO "public"."users" VALUES (7, 'test4', '984634545', 'test4@test.com', 'e99a18c428cb38d5f260853678922e03', 'user', 1);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."assets_asset_id_seq"
OWNED BY "public"."assets"."asset_id";
SELECT setval('"public"."assets_asset_id_seq"', 70, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."brands_brand_id_seq"
OWNED BY "public"."brands"."brand_id";
SELECT setval('"public"."brands_brand_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."config_conf_id_seq"
OWNED BY "public"."config"."conf_id";
SELECT setval('"public"."config_conf_id_seq"', 14, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."config_conf_id_seq1"
OWNED BY "public"."config"."conf_id";
SELECT setval('"public"."config_conf_id_seq1"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."exclusiones_exsite_id_seq"
OWNED BY "public"."exclusiones"."exsite_id";
SELECT setval('"public"."exclusiones_exsite_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."exclusiones_exsite_id_seq1"
OWNED BY "public"."exclusiones"."exsite_id";
SELECT setval('"public"."exclusiones_exsite_id_seq1"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."links_link_id_seq"
OWNED BY "public"."links"."link_id";
SELECT setval('"public"."links_link_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."sitemap_site_id_seq"
OWNED BY "public"."sitemap"."site_id";
SELECT setval('"public"."sitemap_site_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."sitemap_site_id_seq1"
OWNED BY "public"."sitemap"."site_id";
SELECT setval('"public"."sitemap_site_id_seq1"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_user_id_seq"
OWNED BY "public"."users"."user_id";
SELECT setval('"public"."users_user_id_seq"', 7, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_user_id_seq1"
OWNED BY "public"."users"."user_id";
SELECT setval('"public"."users_user_id_seq1"', 1, false);

-- ----------------------------
-- Primary Key structure for table article
-- ----------------------------
ALTER TABLE "public"."article" ADD CONSTRAINT "article_pkey" PRIMARY KEY ("article_id");

-- ----------------------------
-- Primary Key structure for table assets
-- ----------------------------
ALTER TABLE "public"."assets" ADD CONSTRAINT "alertas_pkey" PRIMARY KEY ("asset_id");

-- ----------------------------
-- Primary Key structure for table brands
-- ----------------------------
ALTER TABLE "public"."brands" ADD CONSTRAINT "abrands_pkey" PRIMARY KEY ("brand_id");

-- ----------------------------
-- Auto increment value for config
-- ----------------------------
SELECT setval('"public"."config_conf_id_seq1"', 1, false);

-- ----------------------------
-- Primary Key structure for table config
-- ----------------------------
ALTER TABLE "public"."config" ADD CONSTRAINT "config_pkey" PRIMARY KEY ("conf_id");

-- ----------------------------
-- Auto increment value for exclusiones
-- ----------------------------
SELECT setval('"public"."exclusiones_exsite_id_seq1"', 1, false);

-- ----------------------------
-- Primary Key structure for table exclusiones
-- ----------------------------
ALTER TABLE "public"."exclusiones" ADD CONSTRAINT "exclusiones_pkey" PRIMARY KEY ("exsite_id");

-- ----------------------------
-- Auto increment value for links
-- ----------------------------
SELECT setval('"public"."links_link_id_seq"', 3, true);

-- ----------------------------
-- Primary Key structure for table links
-- ----------------------------
ALTER TABLE "public"."links" ADD CONSTRAINT "links_pkey" PRIMARY KEY ("link_id");

-- ----------------------------
-- Primary Key structure for table proyectos
-- ----------------------------
ALTER TABLE "public"."proyectos" ADD CONSTRAINT "proyectos_pkey" PRIMARY KEY ("proyecto_id");

-- ----------------------------
-- Auto increment value for sitemap
-- ----------------------------
SELECT setval('"public"."sitemap_site_id_seq1"', 1, false);

-- ----------------------------
-- Primary Key structure for table sitemap
-- ----------------------------
ALTER TABLE "public"."sitemap" ADD CONSTRAINT "sitemap_pkey" PRIMARY KEY ("site_id");

-- ----------------------------
-- Auto increment value for users
-- ----------------------------
SELECT setval('"public"."users_user_id_seq1"', 1, false);

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("user_id");
