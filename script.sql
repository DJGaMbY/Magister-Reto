--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

-- Started on 2021-07-16 17:24:54

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 16397)
-- Name: queries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queries (
    ubicacion text NOT NULL,
    distancia integer NOT NULL,
    centro text,
    id integer NOT NULL
);


ALTER TABLE public.queries OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16395)
-- Name: queries_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.queries ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.queries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 202 (class 1259 OID 16416)
-- Name: schools; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schools (
    nombre text NOT NULL,
    codigo_postal integer NOT NULL,
    municipio text NOT NULL,
    provincia text NOT NULL,
    tipo text NOT NULL,
    cursos text NOT NULL,
    link_web text,
    calle text NOT NULL,
    telefono integer NOT NULL
);


ALTER TABLE public.schools OWNER TO postgres;

--
-- TOC entry 2857 (class 2606 OID 16415)
-- Name: queries queries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queries
    ADD CONSTRAINT queries_pkey PRIMARY KEY (id);


--
-- TOC entry 2859 (class 2606 OID 16425)
-- Name: schools schools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schools
    ADD CONSTRAINT schools_pkey PRIMARY KEY (nombre, codigo_postal);


-- Completed on 2021-07-16 17:24:54

--
-- PostgreSQL database dump complete
--

