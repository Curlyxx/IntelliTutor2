-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-12-2025 a las 01:58:05
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `generador_practicas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades`
--

CREATE TABLE `actividades` (
  `id` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `usuario_id` int(11) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `recurso_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividades`
--

INSERT INTO `actividades` (`id`, `descripcion`, `fecha`, `usuario_id`, `tipo`, `recurso_id`) VALUES
(1, 'Inicio del semestre 2', '2025-11-13 00:01:00', 1, 'semestre', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaciones`
--

CREATE TABLE `asignaciones` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `fecha_asignacion` datetime DEFAULT current_timestamp(),
  `fecha_entrega` datetime DEFAULT NULL,
  `estado` enum('pendiente','entregado','calificado') DEFAULT 'pendiente',
  `archivo_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencias`
--

CREATE TABLE `asistencias` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `estado` enum('presente','ausente','justificado') DEFAULT 'presente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones_finales`
--

CREATE TABLE `calificaciones_finales` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `calificacion_final` decimal(4,2) NOT NULL,
  `practicas_promedio` decimal(4,2) DEFAULT NULL,
  `examenes_promedio` decimal(4,2) DEFAULT NULL,
  `proyectos_promedio` decimal(4,2) DEFAULT NULL,
  `asistencia_porcentaje` decimal(5,2) DEFAULT NULL,
  `fecha_calificacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clases`
--

CREATE TABLE `clases` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `profesor_id` int(11) NOT NULL,
  `semestre` int(11) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `competencias`
--

CREATE TABLE `competencias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `competencias`
--

INSERT INTO `competencias` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Dise?o de BD', 'Capacidad para dise?ar bases de datos eficientes'),
(2, 'Optimizaci?n', 'Habilidad para optimizar consultas y estructuras'),
(3, 'Programaci?n SQL', 'Dominio de SQL y procedimientos almacenados'),
(4, 'Seguridad', 'Implementaci?n de medidas de seguridad en BD');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conceptos`
--

CREATE TABLE `conceptos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `materia_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `conceptos`
--

INSERT INTO `conceptos` (`id`, `nombre`, `descripcion`, `materia_id`) VALUES
(1, 'Bases de datos NoSQL', 'Sistemas de bases de datos no relacionales', 1),
(2, 'Seguridad en BD', 'Implementaci?n de medidas de seguridad', 1),
(3, 'Estructuras de datos', 'Organizaci?n y manipulaci?n de datos', 2),
(4, 'Algoritmos', 'Dise?o y an?lisis de algoritmos', 2),
(5, 'POO', 'Programaci?n Orientada a Objetos', 2),
(6, 'Patrones de dise?o', 'Soluciones comunes a problemas de dise?o', 2),
(7, 'Regresi?n', 'Modelos de regresi?n y predicci?n', 3),
(8, 'Clasificaci?n', 'Algoritmos de clasificaci?n', 3),
(9, 'Clustering', 'Agrupamiento de datos', 3),
(10, 'Redes neuronales', 'Deep learning y redes neuronales', 3),
(11, 'Criptograf?a', 'T?cnicas de cifrado y seguridad', 4),
(12, 'Seguridad en redes', 'Protecci?n de redes y comunicaciones', 4),
(13, 'Ethical Hacking', 'Pruebas de penetraci?n', 4),
(14, 'Forense digital', 'An?lisis forense de sistemas', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contenido_generado`
--

CREATE TABLE `contenido_generado` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `contenido` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`contenido`)),
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `criterios_evaluacion`
--

CREATE TABLE `criterios_evaluacion` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `practicas_porcentaje` decimal(5,2) NOT NULL DEFAULT 40.00,
  `examenes_porcentaje` decimal(5,2) NOT NULL DEFAULT 30.00,
  `proyectos_porcentaje` decimal(5,2) NOT NULL DEFAULT 20.00,
  `asistencia_porcentaje` decimal(5,2) NOT NULL DEFAULT 10.00,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `criterios_evaluacion`
--

INSERT INTO `criterios_evaluacion` (`id`, `grupo_id`, `practicas_porcentaje`, `examenes_porcentaje`, `proyectos_porcentaje`, `asistencia_porcentaje`, `fecha_creacion`) VALUES
(1, 1, 40.00, 30.00, 20.00, 10.00, '2025-11-12 22:33:44'),
(2, 2, 40.00, 30.00, 20.00, 10.00, '2025-11-13 00:00:37'),
(3, 3, 40.00, 30.00, 20.00, 10.00, '2025-11-23 20:28:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-24 03:11:33.363390'),
(2, 'auth', '0001_initial', '2025-11-24 03:11:34.178371'),
(3, 'admin', '0001_initial', '2025-11-24 03:11:34.366018'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-24 03:11:34.385208'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-24 03:11:34.399221'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-24 03:11:34.471397'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-24 03:11:34.561216'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-24 03:11:34.581562'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-24 03:11:34.593223'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-24 03:11:34.655692'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-24 03:11:34.663941'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-24 03:11:34.679470'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-24 03:11:34.696583'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-24 03:11:34.739380'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-24 03:11:34.761748'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-24 03:11:34.775159'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-24 03:11:34.798252'),
(18, 'sessions', '0001_initial', '2025-11-24 03:11:34.848047');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('pxg7gngpdqqvatud14g31u6odzr0xrug', '.eJw1jEsKAjEQBa8y9DqIGWTArBTceobQJA8N5ANJZxgU7y7BcVnUq_em3lBt8GTmo_pB5gQydI3YphuvIfJ0R_Z40T5A4hDJEEdsl8eAgyvpb2uJI0eT7gNnwS722xFpUpR7Qi3WdWRhMnpeTstZa60oNMtdnsgSHAs8Gakdny-MPzp3:1vQaQL:zwtUQXSCVuNTX62oWu3H8cuTDA2e_1LCoaoQ6AoASdk', '2025-12-17 00:08:49.359733');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ediciones_perfil`
--

CREATE TABLE `ediciones_perfil` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `fecha_edicion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entregas`
--

CREATE TABLE `entregas` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `fecha_entrega` datetime NOT NULL,
  `estado` enum('pendiente','revisada','retroalimentada','calificado','entregado') NOT NULL,
  `archivos_url` text DEFAULT NULL,
  `calificacion` decimal(5,2) DEFAULT NULL,
  `contenido` text DEFAULT NULL,
  `evaluacion_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entregas`
--

INSERT INTO `entregas` (`id`, `practica_id`, `estudiante_id`, `fecha_entrega`, `estado`, `archivos_url`, `calificacion`, `contenido`, `evaluacion_id`) VALUES
(1, 1, 3, '2025-11-12 23:49:04', 'entregado', 'entrega_1_1763012944.py', NULL, 'sdf', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estilos_aprendizaje`
--

CREATE TABLE `estilos_aprendizaje` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estilos_aprendizaje`
--

INSERT INTO `estilos_aprendizaje` (`id`, `nombre`, `descripcion`, `fecha_creacion`) VALUES
(1, 'visual', 'Aprende mejor a trav?s de im?genes, diagramas y representaciones visuales', '2025-11-12 21:40:32'),
(2, 'auditivo', 'Aprende mejor a trav?s de la escucha y la discusi?n verbal', '2025-11-12 21:40:32'),
(3, 'kinestesico', 'Aprende mejor a trav?s de la experiencia pr?ctica y la actividad f?sica', '2025-11-12 21:40:32'),
(4, 'lectura_escritura', 'Aprende mejor a trav?s de la lectura y la escritura de textos', '2025-11-12 21:40:32'),
(5, 'multimodal', 'Aprende utilizando una combinaci?n de estilos de aprendizaje', '2025-11-12 21:40:32'),
(6, 'anal?tico', 'Aprende mejor a trav?s del an?lisis l?gico y la descomposici?n de conceptos', '2025-11-12 21:40:32'),
(7, 'hol?stico', 'Aprende mejor viendo el panorama completo y las conexiones entre conceptos', '2025-11-12 21:40:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluaciones`
--

CREATE TABLE `evaluaciones` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `evaluador_id` int(11) NOT NULL,
  `fecha_evaluacion` datetime NOT NULL,
  `estado` enum('pendiente','en_proceso','completada','revisada','calificado','entregado') NOT NULL,
  `calificacion` decimal(5,2) DEFAULT NULL,
  `comentarios` text DEFAULT NULL,
  `uso_ia` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `evaluaciones`
--

INSERT INTO `evaluaciones` (`id`, `practica_id`, `estudiante_id`, `evaluador_id`, `fecha_evaluacion`, `estado`, `calificacion`, `comentarios`, `uso_ia`) VALUES
(1, 1, 2, 4, '2025-11-12 22:46:09', 'pendiente', NULL, NULL, 1),
(2, 1, 3, 4, '2025-11-12 22:46:09', 'entregado', NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `evaluaciones_ia`
--

CREATE TABLE `evaluaciones_ia` (
  `id` int(11) NOT NULL,
  `evaluacion_id` int(11) NOT NULL,
  `contenido_original` text NOT NULL,
  `calificacion` decimal(4,2) NOT NULL,
  `retroalimentacion` text NOT NULL,
  `estilo_aprendizaje_id` int(11) DEFAULT NULL,
  `criterios_evaluados` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`criterios_evaluados`)),
  `errores_detectados` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`errores_detectados`)),
  `recursos_recomendados` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`recursos_recomendados`)),
  `fecha_evaluacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `materia_id` int(11) NOT NULL,
  `semestre_id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `activo` tinyint(1) DEFAULT 1,
  `turno` varchar(20) DEFAULT 'matutino',
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `evaluacion_finalizada` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grupos`
--

INSERT INTO `grupos` (`id`, `nombre`, `descripcion`, `materia_id`, `semestre_id`, `profesor_id`, `fecha_creacion`, `activo`, `turno`, `fecha_inicio`, `fecha_fin`, `evaluacion_finalizada`) VALUES
(1, 'grupo1', 'el primer grupo', 1, 3, 4, '2025-11-12 22:33:44', 1, 'matutino', '2025-11-13', '2025-11-27', 0),
(2, 'ASDGGGG', 'second group', 4, 2, 4, '2025-11-13 00:00:37', 1, 'vespertino', '2025-11-20', '2025-11-28', 0),
(3, 'progamacion I', 'Curso de python', 3, 2, 4, '2025-11-23 20:28:43', 1, 'matutino', '2025-11-21', '2025-11-27', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupo_estudiante`
--

CREATE TABLE `grupo_estudiante` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `fecha_inscripcion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupo_miembros`
--

CREATE TABLE `grupo_miembros` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grupo_miembros`
--

INSERT INTO `grupo_miembros` (`id`, `grupo_id`, `usuario_id`, `rol`) VALUES
(1, 1, 2, 'estudiante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `herramientas`
--

CREATE TABLE `herramientas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `herramientas`
--

INSERT INTO `herramientas` (`id`, `nombre`, `descripcion`, `tipo`, `url`) VALUES
(1, 'MySQL', 'Sistema de gesti?n de bases de datos relacionales', 'DBMS', NULL),
(2, 'PostgreSQL', 'Sistema de BD relacional avanzado', 'DBMS', NULL),
(3, 'MongoDB', 'Base de datos NoSQL', 'NoSQL', NULL),
(4, 'DBeaver', 'Cliente universal de bases de datos', 'Cliente', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcos_desbloqueados`
--

CREATE TABLE `marcos_desbloqueados` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `marco_id` int(11) NOT NULL,
  `fecha_desbloqueo` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcos_perfil`
--

CREATE TABLE `marcos_perfil` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `clase_css` varchar(100) NOT NULL,
  `condicion_desbloqueo` varchar(255) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marcos_perfil`
--

INSERT INTO `marcos_perfil` (`id`, `nombre`, `descripcion`, `imagen_url`, `clase_css`, `condicion_desbloqueo`, `fecha_creacion`) VALUES
(1, 'Marco B?sico', 'Marco b?sico para estudiantes de primer semestre', NULL, 'marco-basico', 'Completar primer semestre', '2025-11-12 21:40:32'),
(2, 'Marco Segundo Semestre', 'Marco para estudiantes de segundo semestre', NULL, 'marco-segundo-semestre', 'Completar segundo semestre', '2025-11-12 21:40:32'),
(3, 'Marco Tercer Semestre', 'Marco para estudiantes de tercer semestre', NULL, 'marco-tercer-semestre', 'Completar tercer semestre', '2025-11-12 21:40:32'),
(4, 'Marco Cuarto Semestre', 'Marco para estudiantes de cuarto semestre', NULL, 'marco-cuarto-semestre', 'Completar cuarto semestre', '2025-11-12 21:40:32'),
(5, 'Marco Quinto Semestre', 'Marco para estudiantes de quinto semestre', NULL, 'marco-quinto-semestre', 'Completar quinto semestre', '2025-11-12 21:40:32'),
(6, 'Marco Sexto Semestre', 'Marco para estudiantes de sexto semestre', NULL, 'marco-sexto-semestre', 'Completar sexto semestre', '2025-11-12 21:40:32'),
(7, 'Marco S?ptimo Semestre', 'Marco para estudiantes de s?ptimo semestre', NULL, 'marco-septimo-semestre', 'Completar s?ptimo semestre', '2025-11-12 21:40:32'),
(8, 'Marco Octavo Semestre', 'Marco para estudiantes de octavo semestre', NULL, 'marco-octavo-semestre', 'Completar octavo semestre', '2025-11-12 21:40:32'),
(9, 'Marco Noveno Semestre', 'Marco para estudiantes de noveno semestre', NULL, 'marco-noveno-semestre', 'Completar noveno semestre', '2025-11-12 21:40:32'),
(10, 'Marco de Excelencia', 'Marco especial para estudiantes con promedio superior a 9.5', NULL, 'marco-excelencia', 'Obtener promedio superior a 9.5', '2025-11-12 21:40:32'),
(11, 'Marco Responsable', 'Marco para estudiantes que llevan 3 meses sin tareas atrasadas', NULL, 'marco-responsable', 'Mantener 3 meses sin tareas atrasadas', '2025-11-12 21:40:32'),
(12, 'Marco N?mero Uno', 'Marco exclusivo para el estudiante con mejor promedio de su clase', NULL, 'marco-numero-uno', 'Ser el estudiante con mejor promedio de la clase', '2025-11-12 21:40:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `creditos` int(11) DEFAULT 8
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id`, `nombre`, `descripcion`, `creditos`) VALUES
(1, 'Base de datos', 'Fundamentos y aplicaciones de bases de datos 2', 8),
(2, 'Programaci?n', 'Programaci?n y desarrollo de software', 8),
(3, 'Machine Learning', 'Aprendizaje autom?tico y an?lisis de datos', 8),
(4, 'Seguridad Inform?tica', 'Seguridad de sistemas y redes', 8),
(6, 'Cocina', 'tareas de cocina', 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo_pesos`
--

CREATE TABLE `modelo_pesos` (
  `id` int(11) NOT NULL,
  `nombre_modelo` varchar(100) NOT NULL,
  `ruta_pesos` varchar(255) NOT NULL,
  `version` varchar(50) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `niveles`
--

CREATE TABLE `niveles` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `niveles`
--

INSERT INTO `niveles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'B?sico', 'Nivel fundamental de conocimientos'),
(2, 'Intermedio', 'Nivel medio de conocimientos'),
(3, 'Avanzado', 'Nivel experto de conocimientos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `mensaje` text NOT NULL,
  `leida` tinyint(1) DEFAULT 0,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_administrador`
--

CREATE TABLE `perfiles_administrador` (
  `id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `cargo` varchar(100) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_estudiante`
--

CREATE TABLE `perfiles_estudiante` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `semestre` int(11) NOT NULL,
  `facultad` varchar(100) NOT NULL,
  `carrera` varchar(100) NOT NULL,
  `estilos_aprendizaje` varchar(255) DEFAULT NULL,
  `marco_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfiles_estudiante`
--

INSERT INTO `perfiles_estudiante` (`id`, `estudiante_id`, `semestre`, `facultad`, `carrera`, `estilos_aprendizaje`, `marco_id`, `fecha_creacion`, `fecha_actualizacion`) VALUES
(1, 3, 1, 'FES Cuautitlán', 'informatica', 'visual', NULL, '2025-11-12 23:30:11', NULL),
(2, 19, 7, 'Ingeniería', 'informatica', 'auditivo,lectura_escritura,colaborativo', NULL, '2025-11-30 19:15:11', '2025-11-30 19:15:13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_profesor`
--

CREATE TABLE `perfiles_profesor` (
  `id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  `grado_academico` varchar(100) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plantillas`
--

CREATE TABLE `plantillas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `contenido` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`contenido`)),
  `autor_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `categoria` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practicas`
--

CREATE TABLE `practicas` (
  `id` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `materia_id` int(11) NOT NULL,
  `nivel_id` int(11) NOT NULL,
  `autor_id` int(11) NOT NULL,
  `concepto_id` int(11) DEFAULT NULL,
  `herramienta_id` int(11) DEFAULT NULL,
  `objetivo` text NOT NULL,
  `introduccion` text DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_entrega` datetime NOT NULL,
  `tiempo_estimado` int(11) NOT NULL,
  `estado` enum('Pendiente','Completado','Cancelado') NOT NULL DEFAULT 'Pendiente',
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `uso_ia` tinyint(1) DEFAULT 0,
  `grupo_id` int(11) DEFAULT NULL,
  `tipo_asignacion` enum('practica','examen','proyecto') DEFAULT 'practica'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `practicas`
--

INSERT INTO `practicas` (`id`, `titulo`, `materia_id`, `nivel_id`, `autor_id`, `concepto_id`, `herramienta_id`, `objetivo`, `introduccion`, `descripcion`, `fecha_entrega`, `tiempo_estimado`, `estado`, `fecha_creacion`, `uso_ia`, `grupo_id`, `tipo_asignacion`) VALUES
(1, 'Introducción a algoritmos', 2, 2, 4, 4, 1, 'Aprender a crear algoritmos', NULL, NULL, '2025-11-21 00:00:00', 24, 'Pendiente', '2025-11-12 22:46:09', 1, 1, 'practica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practica_competencia`
--

CREATE TABLE `practica_competencia` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `competencia_id` int(11) NOT NULL,
  `nivel` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `practica_prerequisitos`
--

CREATE TABLE `practica_prerequisitos` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `competencia_id` int(11) NOT NULL,
  `nivel_requerido` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recursos_aprendizaje`
--

CREATE TABLE `recursos_aprendizaje` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `tipo_recurso` varchar(50) NOT NULL,
  `estilo_aprendizaje_id` int(11) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recursos_practica`
--

CREATE TABLE `recursos_practica` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `url` text NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados_aprendizaje`
--

CREATE TABLE `resultados_aprendizaje` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `competencia_id` int(11) NOT NULL,
  `nivel_logrado` int(11) NOT NULL,
  `evidencias` text NOT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `retroalimentacion`
--

CREATE TABLE `retroalimentacion` (
  `id` int(11) NOT NULL,
  `entrega_id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `comentario` text NOT NULL,
  `aspecto` varchar(100) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rubricas`
--

CREATE TABLE `rubricas` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `criterio` varchar(200) NOT NULL,
  `descripcion` text NOT NULL,
  `puntaje_maximo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rubrica_niveles`
--

CREATE TABLE `rubrica_niveles` (
  `id` int(11) NOT NULL,
  `rubrica_id` int(11) NOT NULL,
  `nivel` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `puntaje` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `semestres`
--

CREATE TABLE `semestres` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `semestres`
--

INSERT INTO `semestres` (`id`, `nombre`, `fecha_inicio`, `fecha_fin`, `activo`, `fecha_creacion`) VALUES
(1, '2023-1', '2023-08-07', '2023-12-15', 0, '2025-11-12 21:40:32'),
(2, '2023-2', '2024-01-29', '2024-06-07', 1, '2025-11-12 21:40:32'),
(3, '2024-1', '2024-08-05', '2024-12-13', 0, '2025-11-12 21:40:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes_registro`
--

CREATE TABLE `solicitudes_registro` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol_solicitado` enum('administrador','profesor','estudiante') NOT NULL,
  `estado` enum('pendiente','aprobada','rechazada') DEFAULT 'pendiente',
  `fecha_solicitud` datetime DEFAULT current_timestamp(),
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `solicitudes_registro`
--

INSERT INTO `solicitudes_registro` (`id`, `nombre`, `email`, `password_hash`, `rol_solicitado`, `estado`, `fecha_solicitud`, `password`) VALUES
(1, 'Lex', 'haroldcharold2016@gmail.com', 'scrypt:32768:8:1$4CUaEobiE2LieyN8$86d78cc79c272c9f85afd4342e7d6611af4e393750e807660fc967dc99c287428ad027936c33197c4a8334d52f9f1fbaa923a90eb2f84d54dc2875d97016761a', 'administrador', 'rechazada', '2025-11-12 21:49:47', 'comida123'),
(2, 'profe2', 'prfo4@gmail.com', 'scrypt:32768:8:1$op2Ue6J45j3EE0AQ$77e68dc47a8f6843416a3072d6cdb0c0171a5381aa799529bc1257b9a5f37af1c77a7f7ca53413429cd85b8cb289092288597199d1134dd0187973596a3528d0', 'profesor', 'aprobada', '2025-11-23 20:32:59', '346234');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiempo_registrado`
--

CREATE TABLE `tiempo_registrado` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `tiempo` float NOT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(70) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('estudiante','profesor','admin','administrador') NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `numero_cuenta` int(9) DEFAULT NULL,
  `perfil_completado` tinyint(1) DEFAULT 0,
  `telefono` varchar(20) DEFAULT NULL,
  `usuario` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `password_hash`, `rol`, `fecha_creacion`, `numero_cuenta`, `perfil_completado`, `telefono`, `usuario`) VALUES
(1, 'Alex1', '', '', 'scrypt:32768:8:1$wHerJajKbxHfcXy8$e1bbc0e92d05f34ef63a8f5ba1aacb24df08ebc4c967e32dd94d8582a4fa45c5416f88ba63e6a53d2cb2a6992b8d78b4a97e26357497184d7de9f2d2e370524c', 'administrador', '2025-11-12 21:41:01', 254935503, 0, NULL, ''),
(2, 'user1', '', '2@gmail.com', 'scrypt:32768:8:1$c2XPUyl6kUOPYJ1e$aebea6b327173c05ebb596b83269e112c0c6fc40e6b0bbc2a58db78ce36defa8be1f968514068daedc7ede5466a94b3e4454204cb8e3983a61979bcd805b9b92', 'estudiante', '2025-11-12 22:18:59', 954130566, 0, NULL, ''),
(3, 'user2', '', '3@gmail.com', 'scrypt:32768:8:1$ZWgWB0CfJnNwSVpB$22ce229d60314379d6aca0e1bbe4bdb5ea30e61591df9c252e5d0fe84a8ee02f18920f93525b7b67f938501d6d43d25e3286dc1423964ff3140f4f2155670aeb', 'estudiante', '2025-11-12 22:19:26', 942219917, 1, NULL, ''),
(4, 'user3', '', '4@gmail.com', 'scrypt:32768:8:1$9QKNaF36XGYZrc1p$39e594aaef4c6677706f65224700a2e03ee894fcd79f93cad321e865bea1fdfc3e5ac4f9dc2d840d027a4774b75deb56b8fab38a63b741146cbf227ac18ce312', 'profesor', '2025-11-12 22:21:16', 408542267, 0, NULL, ''),
(5, 'profe2', '', 'prfo4@gmail.com', 'scrypt:32768:8:1$op2Ue6J45j3EE0AQ$77e68dc47a8f6843416a3072d6cdb0c0171a5381aa799529bc1257b9a5f37af1c77a7f7ca53413429cd85b8cb289092288597199d1134dd0187973596a3528d0', 'profesor', '2025-11-23 20:33:39', 317093931, 0, NULL, ''),
(7, 'user1', '', '33@gmail.com', 'scrypt:32768:8:1$6xz0v0Fc9ACnRBTd$f886f47be3e086c72b78c5ba0a20118417858499152285db30ddee07fb0b3a058bcb8b0c443eefcb8f8040d4718434d16a4884d160fe4a77914995f5d74da332', 'estudiante', '2025-11-24 18:30:39', 409051677, 0, NULL, ''),
(11, '1 1', '', '1@gmai.com', 'scrypt:16384:8:1$3e82e3093ceba214c7f5ba59343966d3$2777895424b910168e40bca4163fc03b0b3a2c01beaf620d528400df88f47b833c446199e63437e6214ce70c219177c6866eec5a26da5a2f03e57b47bf3c5ef7', 'estudiante', '2025-11-30 15:48:42', 988765297, 0, NULL, '1'),
(12, '12 12', '', '12@gmail.com', 'scrypt:16384:8:1$1eead29de4962f64816cb6718786098d$aa4b7d0a1e2a56349f5b94e91fc344c718b34011d4aa69b87c1cd1db264e23d187a5ebb61b48df73376cae06701b190fc22e67c4261dbecd2a10f79fcd0560b3', 'estudiante', '2025-11-30 15:55:45', 313515020, 0, NULL, '12'),
(13, '123 123', '', '123@gmial.com', 'scrypt:16384:8:1$fabecea8b7c574cd73a21e2ce96e05c8$dd659735d9f6c5ed5afdeb1bf2068926cf8501e6ab19450fa88b2fc48f46784c1226c2959dc413fb42d5aabd9fdd8f5a75bc88ff231f528163e43742a933e6ce', 'estudiante', '2025-11-30 16:05:18', 118733573, 0, NULL, '123'),
(14, '44 44', '', '44@gmas', 'scrypt:16384:8:1$6285d110f7d3c7e568bd7f53489b3078$86a332f77dc91ea869d3158058eb304ff2890d07cb6f615b23e1fbdf53938e412d41aca9b976aa403a75ba1862cbd4f0911e4aafcb352a8d3630fb3710de7a97', 'estudiante', '2025-11-30 16:09:23', 547638346, 0, NULL, '44'),
(15, '45', '45', '45@asd', 'scrypt:16384:8:1$95d2387c24571168b0f1d8939830a676$3a01a921996c1742eb2640eec92286f3a5fdfe31992da424000ed0a0a57f62a33c42de4256e6aa07a289776fca712661f0acab4ea807ecad9a77e3acd5240ffd', 'estudiante', '2025-11-30 16:17:48', 118411438, 0, NULL, '45'),
(16, 'qw', 'qw', 'qw@ew', 'scrypt:16384:8:1$95d1cb5aa7238a55c9abe48350ae8cde$8748b1b22a33bde933c183fed247c6bc3fe855e39d90a0376af23ff8313c1fb1dc2ca9952b42bbfa192bc0c475803290d63c575d0ba03db1c307f049944e8b96', 'estudiante', '2025-11-30 18:05:46', 227918694, 0, NULL, 'qw'),
(17, 'user1', 'asd', 'asd@asd', 'scrypt:16384:8:1$1b04df71f694b96d1c65a0e2fb01b489$ee494c06a59b7063e5a695eb0f6c474b918a276c839248d017ed858fa16b2dd234578896a087cf254eb26ac318b505c9af37f5e236dc1676ca966fdb4e3209dd', 'estudiante', '2025-11-30 18:10:56', 399009850, 0, NULL, 'cc'),
(18, 'xx', 'xx', 'xx@asd', 'scrypt:16384:8:1$c29dc3acb3b491f6fc17ba6faedde27d$8a56a21e61d8ea854d79a85cc982b209904c8be63e9f269cecbe1c17472168168326bd75706dbbb45ce55b5caa9876d5be86ddec3b543e217f8ee0bb5249f870', 'estudiante', '2025-11-30 18:12:48', 373941731, 0, NULL, 'xx'),
(19, 'user5', '', '5@gmail.com', 'scrypt:32768:8:1$qoi74cV055SnsNU9$3e737b70ac51738146961a211a00a31add320293236277bcffa02b86c692879a0eb658d3dd58e7c4f0c647e24c04442f010f2c0f14f9b9880e13c49e21b532c8', 'estudiante', '2025-11-30 19:09:33', 933939988, 1, NULL, ''),
(20, 'Alex', 'Davila Mendez', 'alex@gmail.com', 'scrypt:16384:8:1$e2eebe782c716f27b1a90366b07f583e$a48aa3272ee0ee9c4cad0765b28f12e65ea8839138f8e21ad6ce0a5940271fb6af3791c99f54458ad2d6184125f6e6c893a43ff5d0641331b482059ce37d71eb', 'estudiante', '2025-12-02 18:07:14', 126469111, 0, NULL, 'alex1');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `versiones`
--

CREATE TABLE `versiones` (
  `id` int(11) NOT NULL,
  `practica_id` int(11) NOT NULL,
  `contenido` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`contenido`)),
  `autor_id` int(11) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `numero_version` int(11) NOT NULL,
  `cambios` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_asistencia` (`estudiante_id`,`grupo_id`,`fecha`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `calificaciones_finales`
--
ALTER TABLE `calificaciones_finales`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_estudiante_grupo` (`estudiante_id`,`grupo_id`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- Indices de la tabla `clases`
--
ALTER TABLE `clases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profesor_id` (`profesor_id`);

--
-- Indices de la tabla `competencias`
--
ALTER TABLE `competencias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `conceptos`
--
ALTER TABLE `conceptos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `materia_id` (`materia_id`);

--
-- Indices de la tabla `contenido_generado`
--
ALTER TABLE `contenido_generado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`);

--
-- Indices de la tabla `criterios_evaluacion`
--
ALTER TABLE `criterios_evaluacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `ediciones_perfil`
--
ALTER TABLE `ediciones_perfil`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `entregas`
--
ALTER TABLE `entregas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `estudiante_id` (`estudiante_id`),
  ADD KEY `evaluacion_id` (`evaluacion_id`);

--
-- Indices de la tabla `estilos_aprendizaje`
--
ALTER TABLE `estilos_aprendizaje`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `estudiante_id` (`estudiante_id`),
  ADD KEY `evaluador_id` (`evaluador_id`);

--
-- Indices de la tabla `evaluaciones_ia`
--
ALTER TABLE `evaluaciones_ia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `evaluacion_id` (`evaluacion_id`),
  ADD KEY `estilo_aprendizaje_id` (`estilo_aprendizaje_id`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `materia_id` (`materia_id`),
  ADD KEY `semestre_id` (`semestre_id`),
  ADD KEY `profesor_id` (`profesor_id`);

--
-- Indices de la tabla `grupo_estudiante`
--
ALTER TABLE `grupo_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_grupo_estudiante` (`grupo_id`,`estudiante_id`),
  ADD KEY `estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `grupo_miembros`
--
ALTER TABLE `grupo_miembros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `herramientas`
--
ALTER TABLE `herramientas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `marcos_desbloqueados`
--
ALTER TABLE `marcos_desbloqueados`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_estudiante_marco` (`estudiante_id`,`marco_id`),
  ADD KEY `marco_id` (`marco_id`);

--
-- Indices de la tabla `marcos_perfil`
--
ALTER TABLE `marcos_perfil`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `modelo_pesos`
--
ALTER TABLE `modelo_pesos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `niveles`
--
ALTER TABLE `niveles`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `perfiles_administrador`
--
ALTER TABLE `perfiles_administrador`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indices de la tabla `perfiles_estudiante`
--
ALTER TABLE `perfiles_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estudiante_id` (`estudiante_id`),
  ADD KEY `marco_id` (`marco_id`);

--
-- Indices de la tabla `perfiles_profesor`
--
ALTER TABLE `perfiles_profesor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `profesor_id` (`profesor_id`);

--
-- Indices de la tabla `plantillas`
--
ALTER TABLE `plantillas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `autor_id` (`autor_id`);

--
-- Indices de la tabla `practicas`
--
ALTER TABLE `practicas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `materia_id` (`materia_id`),
  ADD KEY `nivel_id` (`nivel_id`),
  ADD KEY `autor_id` (`autor_id`),
  ADD KEY `concepto_id` (`concepto_id`),
  ADD KEY `herramienta_id` (`herramienta_id`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- Indices de la tabla `practica_competencia`
--
ALTER TABLE `practica_competencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `competencia_id` (`competencia_id`);

--
-- Indices de la tabla `practica_prerequisitos`
--
ALTER TABLE `practica_prerequisitos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `competencia_id` (`competencia_id`);

--
-- Indices de la tabla `recursos_aprendizaje`
--
ALTER TABLE `recursos_aprendizaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `estilo_aprendizaje_id` (`estilo_aprendizaje_id`);

--
-- Indices de la tabla `recursos_practica`
--
ALTER TABLE `recursos_practica`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`);

--
-- Indices de la tabla `resultados_aprendizaje`
--
ALTER TABLE `resultados_aprendizaje`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `competencia_id` (`competencia_id`);

--
-- Indices de la tabla `retroalimentacion`
--
ALTER TABLE `retroalimentacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `entrega_id` (`entrega_id`),
  ADD KEY `profesor_id` (`profesor_id`);

--
-- Indices de la tabla `rubricas`
--
ALTER TABLE `rubricas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`);

--
-- Indices de la tabla `rubrica_niveles`
--
ALTER TABLE `rubrica_niveles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rubrica_id` (`rubrica_id`);

--
-- Indices de la tabla `semestres`
--
ALTER TABLE `semestres`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `solicitudes_registro`
--
ALTER TABLE `solicitudes_registro`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `tiempo_registrado`
--
ALTER TABLE `tiempo_registrado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `numero_cuenta` (`numero_cuenta`);

--
-- Indices de la tabla `versiones`
--
ALTER TABLE `versiones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `practica_id` (`practica_id`),
  ADD KEY `autor_id` (`autor_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades`
--
ALTER TABLE `actividades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `asistencias`
--
ALTER TABLE `asistencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `calificaciones_finales`
--
ALTER TABLE `calificaciones_finales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `clases`
--
ALTER TABLE `clases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `competencias`
--
ALTER TABLE `competencias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `conceptos`
--
ALTER TABLE `conceptos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `contenido_generado`
--
ALTER TABLE `contenido_generado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `criterios_evaluacion`
--
ALTER TABLE `criterios_evaluacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `ediciones_perfil`
--
ALTER TABLE `ediciones_perfil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `entregas`
--
ALTER TABLE `entregas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `estilos_aprendizaje`
--
ALTER TABLE `estilos_aprendizaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `evaluaciones_ia`
--
ALTER TABLE `evaluaciones_ia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `grupo_estudiante`
--
ALTER TABLE `grupo_estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `grupo_miembros`
--
ALTER TABLE `grupo_miembros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `herramientas`
--
ALTER TABLE `herramientas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `marcos_desbloqueados`
--
ALTER TABLE `marcos_desbloqueados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `marcos_perfil`
--
ALTER TABLE `marcos_perfil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `materias`
--
ALTER TABLE `materias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `modelo_pesos`
--
ALTER TABLE `modelo_pesos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `niveles`
--
ALTER TABLE `niveles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `perfiles_administrador`
--
ALTER TABLE `perfiles_administrador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `perfiles_estudiante`
--
ALTER TABLE `perfiles_estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `perfiles_profesor`
--
ALTER TABLE `perfiles_profesor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `plantillas`
--
ALTER TABLE `plantillas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `practicas`
--
ALTER TABLE `practicas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `practica_competencia`
--
ALTER TABLE `practica_competencia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `practica_prerequisitos`
--
ALTER TABLE `practica_prerequisitos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recursos_aprendizaje`
--
ALTER TABLE `recursos_aprendizaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recursos_practica`
--
ALTER TABLE `recursos_practica`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `resultados_aprendizaje`
--
ALTER TABLE `resultados_aprendizaje`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `retroalimentacion`
--
ALTER TABLE `retroalimentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rubricas`
--
ALTER TABLE `rubricas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `rubrica_niveles`
--
ALTER TABLE `rubrica_niveles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `semestres`
--
ALTER TABLE `semestres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `solicitudes_registro`
--
ALTER TABLE `solicitudes_registro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tiempo_registrado`
--
ALTER TABLE `tiempo_registrado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `versiones`
--
ALTER TABLE `versiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividades`
--
ALTER TABLE `actividades`
  ADD CONSTRAINT `actividades_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `asignaciones`
--
ALTER TABLE `asignaciones`
  ADD CONSTRAINT `asignaciones_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `asignaciones_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `asistencias`
--
ALTER TABLE `asistencias`
  ADD CONSTRAINT `asistencias_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `asistencias_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `calificaciones_finales`
--
ALTER TABLE `calificaciones_finales`
  ADD CONSTRAINT `calificaciones_finales_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `calificaciones_finales_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `clases`
--
ALTER TABLE `clases`
  ADD CONSTRAINT `clases_ibfk_1` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `conceptos`
--
ALTER TABLE `conceptos`
  ADD CONSTRAINT `conceptos_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `contenido_generado`
--
ALTER TABLE `contenido_generado`
  ADD CONSTRAINT `contenido_generado_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `criterios_evaluacion`
--
ALTER TABLE `criterios_evaluacion`
  ADD CONSTRAINT `criterios_evaluacion_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `ediciones_perfil`
--
ALTER TABLE `ediciones_perfil`
  ADD CONSTRAINT `ediciones_perfil_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `entregas`
--
ALTER TABLE `entregas`
  ADD CONSTRAINT `entregas_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entregas_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `entregas_ibfk_3` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `evaluaciones`
--
ALTER TABLE `evaluaciones`
  ADD CONSTRAINT `evaluaciones_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `evaluaciones_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `evaluaciones_ibfk_3` FOREIGN KEY (`evaluador_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `evaluaciones_ia`
--
ALTER TABLE `evaluaciones_ia`
  ADD CONSTRAINT `evaluaciones_ia_ibfk_1` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `evaluaciones_ia_ibfk_2` FOREIGN KEY (`estilo_aprendizaje_id`) REFERENCES `estilos_aprendizaje` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grupos_ibfk_2` FOREIGN KEY (`semestre_id`) REFERENCES `semestres` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grupos_ibfk_3` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `grupo_estudiante`
--
ALTER TABLE `grupo_estudiante`
  ADD CONSTRAINT `grupo_estudiante_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grupo_estudiante_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `grupo_miembros`
--
ALTER TABLE `grupo_miembros`
  ADD CONSTRAINT `grupo_miembros_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grupo_miembros_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `marcos_desbloqueados`
--
ALTER TABLE `marcos_desbloqueados`
  ADD CONSTRAINT `marcos_desbloqueados_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `marcos_desbloqueados_ibfk_2` FOREIGN KEY (`marco_id`) REFERENCES `marcos_perfil` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `perfiles_administrador`
--
ALTER TABLE `perfiles_administrador`
  ADD CONSTRAINT `perfiles_administrador_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `perfiles_estudiante`
--
ALTER TABLE `perfiles_estudiante`
  ADD CONSTRAINT `perfiles_estudiante_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `perfiles_estudiante_ibfk_2` FOREIGN KEY (`marco_id`) REFERENCES `marcos_perfil` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `perfiles_profesor`
--
ALTER TABLE `perfiles_profesor`
  ADD CONSTRAINT `perfiles_profesor_ibfk_1` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `plantillas`
--
ALTER TABLE `plantillas`
  ADD CONSTRAINT `plantillas_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `practicas`
--
ALTER TABLE `practicas`
  ADD CONSTRAINT `practicas_ibfk_1` FOREIGN KEY (`materia_id`) REFERENCES `materias` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `practicas_ibfk_2` FOREIGN KEY (`nivel_id`) REFERENCES `niveles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `practicas_ibfk_3` FOREIGN KEY (`autor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `practicas_ibfk_4` FOREIGN KEY (`concepto_id`) REFERENCES `conceptos` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `practicas_ibfk_5` FOREIGN KEY (`herramienta_id`) REFERENCES `herramientas` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `practicas_ibfk_6` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `practica_competencia`
--
ALTER TABLE `practica_competencia`
  ADD CONSTRAINT `practica_competencia_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `practica_competencia_ibfk_2` FOREIGN KEY (`competencia_id`) REFERENCES `competencias` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `practica_prerequisitos`
--
ALTER TABLE `practica_prerequisitos`
  ADD CONSTRAINT `practica_prerequisitos_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `practica_prerequisitos_ibfk_2` FOREIGN KEY (`competencia_id`) REFERENCES `competencias` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `recursos_aprendizaje`
--
ALTER TABLE `recursos_aprendizaje`
  ADD CONSTRAINT `recursos_aprendizaje_ibfk_1` FOREIGN KEY (`estilo_aprendizaje_id`) REFERENCES `estilos_aprendizaje` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `recursos_practica`
--
ALTER TABLE `recursos_practica`
  ADD CONSTRAINT `recursos_practica_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `resultados_aprendizaje`
--
ALTER TABLE `resultados_aprendizaje`
  ADD CONSTRAINT `resultados_aprendizaje_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `resultados_aprendizaje_ibfk_2` FOREIGN KEY (`competencia_id`) REFERENCES `competencias` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `retroalimentacion`
--
ALTER TABLE `retroalimentacion`
  ADD CONSTRAINT `retroalimentacion_ibfk_1` FOREIGN KEY (`entrega_id`) REFERENCES `entregas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `retroalimentacion_ibfk_2` FOREIGN KEY (`profesor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `rubricas`
--
ALTER TABLE `rubricas`
  ADD CONSTRAINT `rubricas_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `rubrica_niveles`
--
ALTER TABLE `rubrica_niveles`
  ADD CONSTRAINT `rubrica_niveles_ibfk_1` FOREIGN KEY (`rubrica_id`) REFERENCES `rubricas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tiempo_registrado`
--
ALTER TABLE `tiempo_registrado`
  ADD CONSTRAINT `tiempo_registrado_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `versiones`
--
ALTER TABLE `versiones`
  ADD CONSTRAINT `versiones_ibfk_1` FOREIGN KEY (`practica_id`) REFERENCES `practicas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `versiones_ibfk_2` FOREIGN KEY (`autor_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
