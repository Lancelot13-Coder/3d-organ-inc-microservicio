-- Ejecuta esto en Supabase: panel izquierdo -> SQL Editor -> New query
-- Crea la tabla que este microservicio va a leer.

create table if not exists modelos (
    id bigint generated always as identity primary key,
    nombre text not null,
    descripcion text default ' ',
    categoria text not null,
    fecha_registro timestamp with time zone default now(),
    activo boolean default true
);

-- Datos de EJEMPLO para poder probar el microservicio de una vez.

insert into modelos (nombre, descripcion, categoria, activo) values
    ('Modelo de la BioTinta (Bioink)', 'Observa el modelo de la Composición y Microestructura de la Biotinta.', '🦻 Modelos del Oído', true),
    ('Modelo de Ejemplo para Pruebas', 'Este es el Primer Modelo de las Pruebas.', '🤖 Modelos de Prueba', true),
    ('Modelo del Sonido Interno (Trayecto Auditivo)', 'Visualización Dinámica del recorrido de la Onda Sonora desde la Entrada hasta la Transducción Neuronal.', '🦻 Modelos del Oído', true),
    ('Modelo Segundo de Ejemplo', 'Este es Otro Modelo de las Pruebas.', '🤖 Modelos de Prueba', true),
    ('Modelo de la Cóclea (Oído Interno)', 'Modelo 3D de la Cóclea: estructura en espiral responsable de convertir vibraciones en señales neuronales.', '🦻 Modelos del Oído', true);
