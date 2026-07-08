#!/usr/bin/env python3
"""Generate the addon translation template and starter translations.

This is a lightweight extractor for the public repository. The canonical Odoo
export can still be run from an Odoo database, but this script keeps the i18n
files reproducible in environments without a configured Odoo instance.
"""

from __future__ import annotations

import ast
import datetime as dt
import os
import re
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

ADDON = "odoo_agent"
ROOT = Path(ADDON)
I18N = ROOT / "i18n"
LANGS = {
    "es": "Spanish",
    "ca": "Catalan / Valencian",
    "gl": "Galician",
    "eu": "Basque",
}
ODOO_BASE_I18N = [
    Path(path)
    for path in os.getenv("ODOO_BASE_I18N", "").split(os.pathsep)
    if path
]

SKIP_VALUES = {
    "qa-agent",
}
SKIP_PATTERNS = [
    re.compile(r"^%\(action_[^)]+\)d$"),
    re.compile(r"^[a-zA-Z0-9_.]+$"),
]
XML_TEXT_TAGS = {"button", "label", "span", "strong", "p", "div"}
XML_ATTRS = {"string", "help", "title", "placeholder", "sum"}

CUSTOM = {
    "es": {
        "AI Agent": "Agente de IA",
        "AI Agent System": "Sistema de agentes de IA",
        "AI Agent System Dashboard — real-time status overview.": "Panel del sistema de agentes de IA — resumen de estado en tiempo real.",
        "AI Agent management: runtimes, agents, executions, logs, chat, MCP, and stage mapping": "Gestión de agentes de IA: runtimes, agentes, ejecuciones, logs, chat, MCP y mapeo de etapas",
        "Provides a native multi-agent execution architecture inside Odoo. - Agent Runtimes: external machines (N100, Mac Mini, etc.) connected via API - AI Agents: configurable entities with instructions, skills, and runtime assignment - Agent Skills: reusable instruction packs - Agent Executions: repeatable runtime work units linked to project.task - Execution Logs: detailed command history with streaming support - Agent Chat: direct messaging between users and AI agents - Stage Mapping: configurable agent status to project stage mapping - REST API: bidirectional communication with external runtimes": "Proporciona una arquitectura nativa de ejecución multiagente dentro de Odoo. - Runtimes de agentes: máquinas externas conectadas por API - Agentes de IA: entidades configurables con instrucciones, skills y runtime asignado - Skills de agente: paquetes reutilizables de instrucciones - Ejecuciones de agente: unidades de trabajo repetibles vinculadas a project.task - Logs de ejecución: historial detallado con soporte de streaming - Chat de agente: mensajería directa entre usuarios y agentes de IA - Mapeo de etapas: mapeo configurable de estado del agente a etapa de proyecto - API REST: comunicación bidireccional con runtimes externos",
        "Agent setup tip:": "Consejo de configuración del agente:",
        "Runtime tip:": "Consejo de runtime:",
        "Skill tip:": "Consejo de skill:",
        "MCP server tip:": "Consejo de servidor MCP:",
        "Agent execution queued for <b>%s</b>.": "Ejecución de agente en cola para <b>%s</b>.",
        "Agent <b>%s</b> completed task: %s": "El agente <b>%s</b> completó la tarea: %s",
        "Agent <b>%s</b> failed task: %s": "El agente <b>%s</b> falló en la tarea: %s",
        "Agent is working on this task": "El agente está trabajando en esta tarea",
        "Assign an AI agent before sending the task.": "Asigna un agente de IA antes de enviar la tarea.",
        "The selected AI agent must have a runtime.": "El agente de IA seleccionado debe tener un runtime.",
        "The selected agent must have a runtime before creating an execution.": "El agente seleccionado debe tener un runtime antes de crear una ejecución.",
        "Cancellation requested from Odoo.": "Cancelación solicitada desde Odoo.",
        "Short handle used to mention this agent from prompts, for example @qa or @hermes.": "Identificador corto para mencionar este agente desde prompts, por ejemplo @qa o @hermes.",
        "Agents mentioned in the prompt with @handle.": "Agentes mencionados en el prompt con @identificador.",
        "Mention agents in the prompt with @handle to create child executions. Delegations are traceable through Parent Execution and this list.": "Menciona agentes en el prompt con @identificador para crear ejecuciones hijas. Las delegaciones se trazan mediante la ejecución padre y esta lista.",
        "You were mentioned from execution \"%(execution)s\" by agent \"%(agent)s\". Focus only on the part of the task that matches your role. Original prompt: %(prompt)s": "Has sido mencionado desde la ejecución \"%(execution)s\" por el agente \"%(agent)s\". Céntrate sólo en la parte de la tarea que corresponda a tu rol. Prompt original: %(prompt)s",
        "<p><b>%s</b> delegated work to: %s.</p>": "<p><b>%s</b> delegó trabajo a: %s.</p>",
        "<p>Agent <b>%s</b> completed execution <b>%s</b>.</p>": "<p>El agente <b>%s</b> completó la ejecución <b>%s</b>.</p>",
        "<p>Agent <b>%s</b> failed execution <b>%s</b>.</p><p>%s</p>": "<p>El agente <b>%s</b> falló en la ejecución <b>%s</b>.</p><p>%s</p>",
        "<p>Agent execution <b>%s</b> was cancelled.</p>": "<p>La ejecución de agente <b>%s</b> fue cancelada.</p>",
        "<p>Skipped mentioned agents without runtime: %s.</p>": "<p>Se omitieron agentes mencionados sin runtime: %s.</p>",
        "%(parent)s → %(agent)s": "%(parent)s → %(agent)s",
    },
    "ca": {
        "AI Agent": "Agent d'IA",
        "AI Agent System": "Sistema d'agents d'IA",
        "AI Agent System Dashboard — real-time status overview.": "Tauler del sistema d'agents d'IA — resum d'estat en temps real.",
        "AI Agent management: runtimes, agents, executions, logs, chat, MCP, and stage mapping": "Gestió d'agents d'IA: runtimes, agents, execucions, registres, xat, MCP i mapatge d'etapes",
        "Agent setup tip:": "Consell de configuració de l'agent:",
        "Runtime tip:": "Consell de runtime:",
        "Skill tip:": "Consell de skill:",
        "MCP server tip:": "Consell del servidor MCP:",
        "Agent execution queued for <b>%s</b>.": "Execució d'agent en cua per a <b>%s</b>.",
        "Assign an AI agent before sending the task.": "Assigna un agent d'IA abans d'enviar la tasca.",
        "The selected AI agent must have a runtime.": "L'agent d'IA seleccionat ha de tenir un runtime.",
        "The selected agent must have a runtime before creating an execution.": "L'agent seleccionat ha de tenir un runtime abans de crear una execució.",
        "Cancellation requested from Odoo.": "Cancel·lació sol·licitada des d'Odoo.",
        "Short handle used to mention this agent from prompts, for example @qa or @hermes.": "Identificador curt per mencionar aquest agent des dels prompts, per exemple @qa o @hermes.",
        "Agents mentioned in the prompt with @handle.": "Agents mencionats al prompt amb @identificador.",
        "Mention agents in the prompt with @handle to create child executions. Delegations are traceable through Parent Execution and this list.": "Menciona agents al prompt amb @identificador per crear execucions filles. Les delegacions es poden traçar mitjançant l'execució pare i aquesta llista.",
        "You were mentioned from execution \"%(execution)s\" by agent \"%(agent)s\". Focus only on the part of the task that matches your role. Original prompt: %(prompt)s": "Has estat mencionat des de l'execució \"%(execution)s\" per l'agent \"%(agent)s\". Centra't només en la part de la tasca que correspon al teu rol. Prompt original: %(prompt)s",
        "<p><b>%s</b> delegated work to: %s.</p>": "<p><b>%s</b> ha delegat feina a: %s.</p>",
        "<p>Agent <b>%s</b> completed execution <b>%s</b>.</p>": "<p>L'agent <b>%s</b> ha completat l'execució <b>%s</b>.</p>",
        "<p>Agent <b>%s</b> failed execution <b>%s</b>.</p><p>%s</p>": "<p>L'agent <b>%s</b> ha fallat en l'execució <b>%s</b>.</p><p>%s</p>",
        "<p>Agent execution <b>%s</b> was cancelled.</p>": "<p>L'execució d'agent <b>%s</b> s'ha cancel·lat.</p>",
        "<p>Skipped mentioned agents without runtime: %s.</p>": "<p>S'han omès agents mencionats sense runtime: %s.</p>",
        "%(parent)s → %(agent)s": "%(parent)s → %(agent)s",
    },
    "gl": {
        "AI Agent": "Axente de IA",
        "AI Agent System": "Sistema de axentes de IA",
        "AI Agent System Dashboard — real-time status overview.": "Panel do sistema de axentes de IA — resumo de estado en tempo real.",
        "AI Agent management: runtimes, agents, executions, logs, chat, MCP, and stage mapping": "Xestión de axentes de IA: runtimes, axentes, execucións, rexistros, chat, MCP e mapeo de etapas",
        "Agent setup tip:": "Consello de configuración do axente:",
        "Runtime tip:": "Consello de runtime:",
        "Skill tip:": "Consello de skill:",
        "MCP server tip:": "Consello do servidor MCP:",
        "Agent execution queued for <b>%s</b>.": "Execución de axente en cola para <b>%s</b>.",
        "Assign an AI agent before sending the task.": "Asigna un axente de IA antes de enviar a tarefa.",
        "The selected AI agent must have a runtime.": "O axente de IA seleccionado debe ter un runtime.",
        "The selected agent must have a runtime before creating an execution.": "O axente seleccionado debe ter un runtime antes de crear unha execución.",
        "Cancellation requested from Odoo.": "Cancelación solicitada desde Odoo.",
        "Short handle used to mention this agent from prompts, for example @qa or @hermes.": "Identificador curto para mencionar este axente desde prompts, por exemplo @qa ou @hermes.",
        "Agents mentioned in the prompt with @handle.": "Axentes mencionados no prompt con @identificador.",
        "Mention agents in the prompt with @handle to create child executions. Delegations are traceable through Parent Execution and this list.": "Menciona axentes no prompt con @identificador para crear execucións fillas. As delegacións poden trazarse mediante a execución pai e esta lista.",
        "You were mentioned from execution \"%(execution)s\" by agent \"%(agent)s\". Focus only on the part of the task that matches your role. Original prompt: %(prompt)s": "Fuches mencionado desde a execución \"%(execution)s\" polo axente \"%(agent)s\". Céntrate só na parte da tarefa que corresponde ao teu rol. Prompt orixinal: %(prompt)s",
        "<p><b>%s</b> delegated work to: %s.</p>": "<p><b>%s</b> delegou traballo a: %s.</p>",
        "<p>Agent <b>%s</b> completed execution <b>%s</b>.</p>": "<p>O axente <b>%s</b> completou a execución <b>%s</b>.</p>",
        "<p>Agent <b>%s</b> failed execution <b>%s</b>.</p><p>%s</p>": "<p>O axente <b>%s</b> fallou na execución <b>%s</b>.</p><p>%s</p>",
        "<p>Agent execution <b>%s</b> was cancelled.</p>": "<p>A execución de axente <b>%s</b> foi cancelada.</p>",
        "<p>Skipped mentioned agents without runtime: %s.</p>": "<p>Omitíronse axentes mencionados sen runtime: %s.</p>",
        "%(parent)s → %(agent)s": "%(parent)s → %(agent)s",
    },
    "eu": {
        "AI Agent": "IA agentea",
        "AI Agent System": "IA agenteen sistema",
        "AI Agent System Dashboard — real-time status overview.": "IA agenteen sistemaren panela — egoeraren denbora errealeko laburpena.",
        "AI Agent management: runtimes, agents, executions, logs, chat, MCP, and stage mapping": "IA agenteen kudeaketa: runtimeak, agenteak, exekuzioak, logak, txata, MCP eta etaparen mapaketa",
        "Agent setup tip:": "Agentearen konfigurazio aholkua:",
        "Runtime tip:": "Runtime aholkua:",
        "Skill tip:": "Skill aholkua:",
        "MCP server tip:": "MCP zerbitzariaren aholkua:",
        "Agent execution queued for <b>%s</b>.": "Agentearen exekuzioa ilaran jarri da <b>%s</b>rentzat.",
        "Assign an AI agent before sending the task.": "Esleitu IA agente bat zeregina bidali aurretik.",
        "The selected AI agent must have a runtime.": "Hautatutako IA agenteak runtime bat izan behar du.",
        "The selected agent must have a runtime before creating an execution.": "Hautatutako agenteak runtime bat izan behar du exekuzioa sortu aurretik.",
        "Cancellation requested from Odoo.": "Ezeztapena Odootik eskatu da.",
        "Short handle used to mention this agent from prompts, for example @qa or @hermes.": "Promptetatik agente hau aipatzeko identifikatzaile laburra, adibidez @qa edo @hermes.",
        "Agents mentioned in the prompt with @handle.": "Prompt-ean @identifikatzailearekin aipatutako agenteak.",
        "Mention agents in the prompt with @handle to create child executions. Delegations are traceable through Parent Execution and this list.": "Aipatu agenteak prompt-ean @identifikatzailearekin exekuzio semeak sortzeko. Delegazioak guraso exekuzioaren eta zerrenda honen bidez trazagarriak dira.",
        "You were mentioned from execution \"%(execution)s\" by agent \"%(agent)s\". Focus only on the part of the task that matches your role. Original prompt: %(prompt)s": "\"%(agent)s\" agenteak \"%(execution)s\" exekuziotik aipatu zaitu. Zure rolari dagokion zeregin zatian bakarrik jarri arreta. Jatorrizko prompt-a: %(prompt)s",
        "<p><b>%s</b> delegated work to: %s.</p>": "<p><b>%s</b> agenteak lana delegatu dio honi: %s.</p>",
        "<p>Agent <b>%s</b> completed execution <b>%s</b>.</p>": "<p><b>%s</b> agenteak <b>%s</b> exekuzioa osatu du.</p>",
        "<p>Agent <b>%s</b> failed execution <b>%s</b>.</p><p>%s</p>": "<p><b>%s</b> agenteak huts egin du <b>%s</b> exekuzioan.</p><p>%s</p>",
        "<p>Agent execution <b>%s</b> was cancelled.</p>": "<p><b>%s</b> agentearen exekuzioa ezeztatu da.</p>",
        "<p>Skipped mentioned agents without runtime: %s.</p>": "<p>Runtime gabeko aipatutako agenteak saltatu dira: %s.</p>",
        "%(parent)s → %(agent)s": "%(parent)s → %(agent)s",
    },
}

TERM_MAP = {
    "es": {
        "Agent": "Agente", "Agents": "Agentes", "Execution": "Ejecución", "Executions": "Ejecuciones",
        "Runtime": "Runtime", "Runtimes": "Runtimes", "Log": "Log", "Logs": "Logs", "Skill": "Skill", "Skills": "Skills",
        "Task": "Tarea", "Tasks": "Tareas", "Project": "Proyecto", "Status": "Estado", "Description": "Descripción",
        "Instructions": "Instrucciones", "Message": "Mensaje", "Command": "Comando", "Company": "Compañía", "Name": "Nombre",
        "Active": "Activo", "Queued": "En cola", "Running": "Ejecutándose", "Completed": "Completado", "Failed": "Fallido",
        "Cancelled": "Cancelado", "Pending": "Pendiente", "Online": "En línea", "Offline": "Desconectado", "Idle": "Inactivo",
        "Error": "Error", "Errors": "Errores", "Warnings": "Advertencias", "Start": "Iniciar", "Cancel": "Cancelar",
        "Retry": "Reintentar", "Complete": "Completar", "Fail": "Marcar como fallido", "Title": "Título", "Timestamp": "Fecha y hora",
    },
    "ca": {
        "Agent": "Agent", "Agents": "Agents", "Execution": "Execució", "Executions": "Execucions",
        "Runtime": "Runtime", "Log": "Registre", "Logs": "Registres", "Skill": "Skill", "Skills": "Skills",
        "Task": "Tasca", "Tasks": "Tasques", "Project": "Projecte", "Status": "Estat", "Description": "Descripció",
        "Instructions": "Instruccions", "Message": "Missatge", "Command": "Ordre", "Company": "Companyia", "Name": "Nom",
        "Active": "Actiu", "Queued": "En cua", "Running": "En execució", "Completed": "Completat", "Failed": "Fallat",
        "Cancelled": "Cancel·lat", "Pending": "Pendent", "Online": "En línia", "Offline": "Fora de línia", "Idle": "Inactiu",
        "Error": "Error", "Errors": "Errors", "Warnings": "Avisos", "Start": "Inicia", "Cancel": "Cancel·la",
        "Retry": "Reintenta", "Complete": "Completa", "Fail": "Marca com a fallat", "Title": "Títol", "Timestamp": "Data i hora",
    },
    "gl": {
        "Agent": "Axente", "Agents": "Axentes", "Execution": "Execución", "Executions": "Execucións",
        "Runtime": "Runtime", "Log": "Rexistro", "Logs": "Rexistros", "Skill": "Skill", "Skills": "Skills",
        "Task": "Tarefa", "Tasks": "Tarefas", "Project": "Proxecto", "Status": "Estado", "Description": "Descrición",
        "Instructions": "Instrucións", "Message": "Mensaxe", "Command": "Comando", "Company": "Compañía", "Name": "Nome",
        "Active": "Activo", "Queued": "En cola", "Running": "En execución", "Completed": "Completado", "Failed": "Fallido",
        "Cancelled": "Cancelado", "Pending": "Pendente", "Online": "En liña", "Offline": "Desconectado", "Idle": "Inactivo",
        "Error": "Erro", "Errors": "Erros", "Warnings": "Avisos", "Start": "Iniciar", "Cancel": "Cancelar",
        "Retry": "Reintentar", "Complete": "Completar", "Fail": "Marcar como fallido", "Title": "Título", "Timestamp": "Data e hora",
    },
    "eu": {
        "Agent": "Agentea", "Agents": "Agenteak", "Execution": "Exekuzioa", "Executions": "Exekuzioak",
        "Runtime": "Runtime", "Log": "Loga", "Logs": "Logak", "Skill": "Skilla", "Skills": "Skillak",
        "Task": "Zeregina", "Tasks": "Zereginak", "Project": "Proiektua", "Status": "Egoera", "Description": "Deskribapena",
        "Instructions": "Argibideak", "Message": "Mezua", "Command": "Komandoa", "Company": "Enpresa", "Name": "Izena",
        "Active": "Aktibo", "Queued": "Ilaran", "Running": "Exekutatzen", "Completed": "Osatuta", "Failed": "Huts eginda",
        "Cancelled": "Ezeztatuta", "Pending": "Zain", "Online": "Linean", "Offline": "Lineaz kanpo", "Idle": "Inaktibo",
        "Error": "Errorea", "Errors": "Erroreak", "Warnings": "Abisuak", "Start": "Hasi", "Cancel": "Ezeztatu",
        "Retry": "Saiatu berriro", "Complete": "Osatu", "Fail": "Markatu huts eginda", "Title": "Izenburua", "Timestamp": "Data eta ordua",
    },
}

EXACT_EXTRA = {
    "API Key": {"es": "Clave API", "ca": "Clau API", "gl": "Chave API", "eu": "API gakoa"},
    "API key for runtime authentication": {"es": "Clave API para autenticar el runtime", "ca": "Clau API per autenticar el runtime", "gl": "Chave API para autenticar o runtime", "eu": "Runtimea autentifikatzeko API gakoa"},
    "Active Agents": {"es": "Agentes activos", "ca": "Agents actius", "gl": "Axentes activos", "eu": "Agente aktiboak"},
    "Active Executions": {"es": "Ejecuciones activas", "ca": "Execucions actives", "gl": "Execucións activas", "eu": "Exekuzio aktiboak"},
    "Agent Executions": {"es": "Ejecuciones de agente", "ca": "Execucions d'agent", "gl": "Execucións de axente", "eu": "Agentearen exekuzioak"},
    "Agent Logs": {"es": "Logs de agente", "ca": "Registres d'agent", "gl": "Rexistros de axente", "eu": "Agentearen logak"},
    "MCP Servers": {"es": "Servidores MCP", "ca": "Servidors MCP", "gl": "Servidores MCP", "eu": "MCP zerbitzariak"},
    "Send to Agent": {"es": "Enviar al agente", "ca": "Envia a l'agent", "gl": "Enviar ao axente", "eu": "Bidali agenteari"},
    "Generate API Key": {"es": "Generar clave API", "ca": "Genera clau API", "gl": "Xerar chave API", "eu": "Sortu API gakoa"},
    "Waiting for Input": {"es": "Esperando entrada", "ca": "Esperant entrada", "gl": "Agardando entrada", "eu": "Sarreraren zain"},
    "Max Concurrent Executions": {"es": "Ejecuciones concurrentes máximas", "ca": "Execucions concurrents màximes", "gl": "Execucións concorrentes máximas", "eu": "Gehieneko exekuzio paraleloak"},
    "Retry Limit": {"es": "Límite de reintentos", "ca": "Límit de reintents", "gl": "Límite de reintentos", "eu": "Berriro saiatzeko muga"},
    "Timeout (seconds)": {"es": "Timeout (segundos)", "ca": "Timeout (segons)", "gl": "Timeout (segundos)", "eu": "Timeouta (segundoak)"},
    "Mention Handle": {"es": "Identificador de mención", "ca": "Identificador de menció", "gl": "Identificador de mención", "eu": "Aipamen identifikatzailea"},
    "Runtime:": {"es": "Runtime:", "ca": "Runtime:", "gl": "Runtime:", "eu": "Runtimea:"},
}
for msg, vals in EXACT_EXTRA.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val

MORE_EXACT = {
    "Agents assigned here share this runtime's installed CLIs, MCP connectivity, and local permissions.": {
        "es": "Los agentes asignados aquí comparten las CLI instaladas, la conectividad MCP y los permisos locales de este runtime.",
        "ca": "Els agents assignats aquí comparteixen les CLI instal·lades, la connectivitat MCP i els permisos locals d'aquest runtime.",
        "gl": "Os axentes asignados aquí comparten as CLI instaladas, a conectividade MCP e os permisos locais deste runtime.",
        "eu": "Hemen esleitutako agenteek runtime honen instalatutako CLIak, MCP konektibitatea eta baimen lokalak partekatzen dituzte.",
    },
    "Arguments": {"es": "Argumentos", "ca": "Arguments", "gl": "Argumentos", "eu": "Argumentuak"},
    "Assign this task to an AI agent": {"es": "Asignar esta tarea a un agente de IA", "ca": "Assigna aquesta tasca a un agent d'IA", "gl": "Asignar esta tarefa a un axente de IA", "eu": "Esleitu zeregin hau IA agente bati"},
    "Assign to AI agent...": {"es": "Asignar a agente de IA...", "ca": "Assigna a un agent d'IA...", "gl": "Asignar a un axente de IA...", "eu": "Esleitu IA agente bati..."},
    "Assigned agent": {"es": "Agente asignado", "ca": "Agent assignat", "gl": "Axente asignado", "eu": "Esleitutako agentea"},
    "Attempt": {"es": "Intento", "ca": "Intent", "gl": "Intento", "eu": "Saiakera"},
    "Author": {"es": "Autor", "ca": "Autor", "gl": "Autor", "eu": "Egilea"},
    "Author Type": {"es": "Tipo de autor", "ca": "Tipus d'autor", "gl": "Tipo de autor", "eu": "Egile mota"},
    "Avatar": {"es": "Avatar", "ca": "Avatar", "gl": "Avatar", "eu": "Avatarra"},
    "Cancellation Reason": {"es": "Motivo de cancelación", "ca": "Motiu de cancel·lació", "gl": "Motivo de cancelación", "eu": "Ezeztapen arrazoia"},
    "Capabilities": {"es": "Capacidades", "ca": "Capacitats", "gl": "Capacidades", "eu": "Gaitasunak"},
    "Capabilities are reported by the runtime: supported engines, installed CLIs, MCP support, OS details, and capacity. Use them to avoid assigning work to the wrong machine.": {
        "es": "Las capacidades las informa el runtime: motores soportados, CLI instaladas, soporte MCP, detalles del sistema operativo y capacidad. Úsalas para evitar asignar trabajo a la máquina incorrecta.",
        "ca": "Les capacitats les informa el runtime: motors suportats, CLI instal·lades, suport MCP, detalls del sistema operatiu i capacitat. Fes-les servir per evitar assignar feina a la màquina incorrecta.",
        "gl": "As capacidades infórmaas o runtime: motores soportados, CLI instaladas, soporte MCP, detalles do sistema operativo e capacidade. Úsaas para evitar asignar traballo á máquina incorrecta.",
        "eu": "Gaitasunak runtimeak jakinarazten ditu: onartutako motorrak, instalatutako CLIak, MCP euskarria, sistema eragilearen xehetasunak eta edukiera. Erabili lana makina okerrari ez esleitzeko.",
    },
    "Command executed by the runtime for this agent.": {"es": "Comando ejecutado por el runtime para este agente.", "ca": "Ordre executada pel runtime per a aquest agent.", "gl": "Comando executado polo runtime para este axente.", "eu": "Runtimeak agente honentzat exekutatutako komandoa."},
    "Compatibility field. Use Max Concurrent Executions for new runtime dispatch.": {"es": "Campo de compatibilidad. Usa Ejecuciones concurrentes máximas para el nuevo despacho del runtime.", "ca": "Camp de compatibilitat. Usa Execucions concurrents màximes per al nou despatx del runtime.", "gl": "Campo de compatibilidade. Usa Execucións concorrentes máximas para o novo despacho do runtime.", "eu": "Bateragarritasun eremua. Erabili gehieneko exekuzio paraleloak runtime bidalketa berrirako."},
    "Daemon/CLI version": {"es": "Versión del daemon/CLI", "ca": "Versió del daemon/CLI", "gl": "Versión do daemon/CLI", "eu": "Daemon/CLI bertsioa"},
    "Delegated": {"es": "Delegado", "ca": "Delegat", "gl": "Delegado", "eu": "Delegatua"},
    "Delegations": {"es": "Delegaciones", "ca": "Delegacions", "gl": "Delegacións", "eu": "Delegazioak"},
    "Describe what tools or data this server exposes and which business process it supports.": {"es": "Describe qué herramientas o datos expone este servidor y qué proceso de negocio soporta.", "ca": "Descriu quines eines o dades exposa aquest servidor i quin procés de negoci suporta.", "gl": "Describe que ferramentas ou datos expón este servidor e que proceso de negocio soporta.", "eu": "Deskribatu zer tresna edo datu eskaintzen dituen zerbitzari honek eta zer negozio-prozesu onartzen duen."},
    "Device Info": {"es": "Información del dispositivo", "ca": "Informació del dispositiu", "gl": "Información do dispositivo", "eu": "Gailuaren informazioa"},
    "Each execution is one auditable run against a Project task: queued, running, waiting for input, completed, failed, or cancelled.": {
        "es": "Cada ejecución es una ejecución auditable sobre una tarea de Proyecto: en cola, ejecutándose, esperando entrada, completada, fallida o cancelada.",
        "ca": "Cada execució és una execució auditable sobre una tasca de Projecte: en cua, en execució, esperant entrada, completada, fallada o cancel·lada.",
        "gl": "Cada execución é unha execución auditable sobre unha tarefa de Proxecto: en cola, en execución, agardando entrada, completada, fallida ou cancelada.",
        "eu": "Exekuzio bakoitza Proiektu zeregin baten aurkako exekuzio auditagarria da: ilaran, exekutatzen, sarreraren zain, osatuta, huts eginda edo ezeztatuta.",
    },
    "Engine": {"es": "Motor", "ca": "Motor", "gl": "Motor", "eu": "Motorra"},
    "Environment": {"es": "Entorno", "ca": "Entorn", "gl": "Contorno", "eu": "Ingurunea"},
    "Exit Code": {"es": "Código de salida", "ca": "Codi de sortida", "gl": "Código de saída", "eu": "Irteera kodea"},
    "Explain when to use this skill, required inputs, expected output, and guardrails. These instructions are injected into the agent prompt at execution time.": {
        "es": "Explica cuándo usar esta skill, las entradas requeridas, la salida esperada y los límites. Estas instrucciones se inyectan en el prompt del agente en tiempo de ejecución.",
        "ca": "Explica quan s'ha d'usar aquesta skill, les entrades requerides, la sortida esperada i els límits. Aquestes instruccions s'injecten al prompt de l'agent en temps d'execució.",
        "gl": "Explica cando usar esta skill, as entradas requiridas, a saída esperada e os límites. Estas instrucións inxéctanse no prompt do axente en tempo de execución.",
        "eu": "Azaldu noiz erabili skill hau, beharrezko sarrerak, espero den irteera eta mugak. Argibide hauek agentearen prompt-ean txertatzen dira exekuzioan.",
    },
    "For stdio servers, add one argument per line or a JSON-style list understood by the runtime adapter. Avoid secrets here; use Environment for sensitive values.": {
        "es": "Para servidores stdio, añade un argumento por línea o una lista estilo JSON entendida por el adaptador del runtime. Evita secretos aquí; usa Entorno para valores sensibles.",
        "ca": "Per a servidors stdio, afegeix un argument per línia o una llista d'estil JSON entesa per l'adaptador del runtime. Evita secrets aquí; usa Entorn per a valors sensibles.",
        "gl": "Para servidores stdio, engade un argumento por liña ou unha lista estilo JSON entendida polo adaptador do runtime. Evita segredos aquí; usa Contorno para valores sensibles.",
        "eu": "Stdio zerbitzarietarako, gehitu argumentu bat lerro bakoitzeko edo runtime egokitzaileak ulertzen duen JSON estiloko zerrenda. Ez jarri sekreturik hemen; erabili Ingurunea balio sentikorretarako.",
    },
    "In Progress": {"es": "En progreso", "ca": "En progrés", "gl": "En progreso", "eu": "Abian"},
    "Is Read": {"es": "Leído", "ca": "Llegit", "gl": "Lido", "eu": "Irakurrita"},
    "LLM model to use": {"es": "Modelo LLM a usar", "ca": "Model LLM a usar", "gl": "Modelo LLM a usar", "eu": "Erabili beharreko LLM eredua"},
    "Last Heartbeat": {"es": "Último heartbeat", "ca": "Últim heartbeat", "gl": "Último heartbeat", "eu": "Azken heartbeat-a"},
    "Last Seen": {"es": "Última vez visto", "ca": "Vist per última vegada", "gl": "Visto por última vez", "eu": "Azken aldiz ikusita"},
    "Latest agent execution completed": {"es": "Última ejecución de agente completada", "ca": "Última execució d'agent completada", "gl": "Última execución de axente completada", "eu": "Agentearen azken exekuzioa osatuta"},
    "Latest agent execution failed": {"es": "Última ejecución de agente fallida", "ca": "Última execució d'agent fallada", "gl": "Última execución de axente fallida", "eu": "Agentearen azken exekuzioak huts egin du"},
    "Legacy tracking field. New flows use Agent Executions.": {"es": "Campo de seguimiento heredado. Los flujos nuevos usan Ejecuciones de agente.", "ca": "Camp de seguiment heretat. Els fluxos nous usen Execucions d'agent.", "gl": "Campo de seguimento herdado. Os fluxos novos usan Execucións de axente.", "eu": "Jarraipen eremu zaharra. Fluxu berriek Agentearen exekuzioak erabiltzen dituzte."},
    "Link to an existing Odoo project task": {"es": "Enlace a una tarea de proyecto de Odoo existente", "ca": "Enllaç a una tasca de projecte d'Odoo existent", "gl": "Ligazón a unha tarefa de proxecto de Odoo existente", "eu": "Lehendik dagoen Odoo proiektu zeregin batera esteka"},
    "Linked User": {"es": "Usuario vinculado", "ca": "Usuari vinculat", "gl": "Usuario vinculado", "eu": "Lotutako erabiltzailea"},
    "Log Count": {"es": "Número de logs", "ca": "Nombre de registres", "gl": "Número de rexistros", "eu": "Log kopurua"},
    "MCP servers expose tools and data sources to the agent runtime. Assign only trusted servers and verify their commands, URLs, and environment variables on the runtime host.": {
        "es": "Los servidores MCP exponen herramientas y fuentes de datos al runtime del agente. Asigna sólo servidores de confianza y verifica sus comandos, URL y variables de entorno en el host del runtime.",
        "ca": "Els servidors MCP exposen eines i fonts de dades al runtime de l'agent. Assigna només servidors de confiança i verifica les seves ordres, URL i variables d'entorn al host del runtime.",
        "gl": "Os servidores MCP expoñen ferramentas e fontes de datos ao runtime do axente. Asigna só servidores de confianza e verifica os seus comandos, URL e variables de contorno no host do runtime.",
        "eu": "MCP zerbitzariek tresnak eta datu-iturburuak eskaintzen dizkiote agentearen runtimeari. Esleitu konfiantzazko zerbitzariak bakarrik eta egiaztatu komandoak, URLak eta ingurune-aldagaiak runtime hostean.",
    },
    "Machine ID": {"es": "ID de máquina", "ca": "ID de màquina", "gl": "ID de máquina", "eu": "Makina IDa"},
    "Model": {"es": "Modelo", "ca": "Model", "gl": "Modelo", "eu": "Eredua"},
    "Monitor active and failed agent executions.": {"es": "Monitoriza ejecuciones de agente activas y fallidas.", "ca": "Monitoritza execucions d'agent actives i fallades.", "gl": "Monitoriza execucións de axente activas e fallidas.", "eu": "Monitorizatu agentearen exekuzio aktiboak eta huts egindakoak."},
    "OS, hardware info": {"es": "Información del SO y hardware", "ca": "Informació del SO i maquinari", "gl": "Información do SO e hardware", "eu": "SE eta hardware informazioa"},
    "Optional: link to an Odoo user for permissions": {"es": "Opcional: vincular a un usuario de Odoo para permisos", "ca": "Opcional: vincular a un usuari d'Odoo per a permisos", "gl": "Opcional: vincular a un usuario de Odoo para permisos", "eu": "Aukerakoa: lotu Odoo erabiltzaile batekin baimenetarako"},
    "Prompt": {"es": "Prompt", "ca": "Prompt", "gl": "Prompt", "eu": "Prompt-a"},
    "Requested By": {"es": "Solicitado por", "ca": "Sol·licitat per", "gl": "Solicitado por", "eu": "Eskatzailea"},
    "Result": {"es": "Resultado", "ca": "Resultat", "gl": "Resultado", "eu": "Emaitza"},
    "Result/Output": {"es": "Resultado/Salida", "ca": "Resultat/Sortida", "gl": "Resultado/Saída", "eu": "Emaitza/Irteera"},
    "Server Key": {"es": "Clave del servidor", "ca": "Clau del servidor", "gl": "Chave do servidor", "eu": "Zerbitzari gakoa"},
    "Skills are reusable capability packs injected into the final prompt. Add only the skills this agent needs; too many skills make executions noisy and harder to audit.": {
        "es": "Las skills son paquetes reutilizables de capacidades que se inyectan en el prompt final. Añade sólo las que este agente necesita; demasiadas skills hacen las ejecuciones más ruidosas y difíciles de auditar.",
        "ca": "Les skills són paquets reutilitzables de capacitats que s'injecten al prompt final. Afegeix només les que aquest agent necessita; massa skills fan les execucions més sorolloses i difícils d'auditar.",
        "gl": "As skills son paquetes reutilizables de capacidades que se inxectan no prompt final. Engade só as que este axente necesita; demasiadas skills fan as execucións máis ruidosas e difíciles de auditar.",
        "eu": "Skillak azken prompt-ean txertatzen diren gaitasun-pakete berrerabilgarriak dira. Gehitu agente honek behar dituenak bakarrik; skill gehiegik exekuzioak zaratatsuago eta auditatzeko zailago bihurtzen dituzte.",
    },
    "Started At": {"es": "Iniciado el", "ca": "Iniciat el", "gl": "Iniciado o", "eu": "Hasiera data"},
    "Store environment variables required by the MCP server. Prefer references to runtime-side secrets when possible instead of plain credentials.": {
        "es": "Guarda las variables de entorno requeridas por el servidor MCP. Siempre que sea posible, prefiere referencias a secretos del runtime en lugar de credenciales en claro.",
        "ca": "Desa les variables d'entorn requerides pel servidor MCP. Sempre que sigui possible, prefereix referències a secrets del runtime en lloc de credencials en clar.",
        "gl": "Garda as variables de contorno requiridas polo servidor MCP. Sempre que sexa posible, prefire referencias a segredos do runtime en lugar de credenciais en claro.",
        "eu": "Gorde MCP zerbitzariak behar dituen ingurune-aldagaiak. Ahal denean, erabili runtime aldeko sekretuen erreferentziak kredentzial arrunten ordez.",
    },
    "Subtasks": {"es": "Subtareas", "ca": "Subtasques", "gl": "Subtarefas", "eu": "Azpizereginak"},
    "System prompt / instructions for the agent": {"es": "Prompt de sistema / instrucciones para el agente", "ca": "Prompt de sistema / instruccions per a l'agent", "gl": "Prompt de sistema / instrucións para o axente", "eu": "Sistemaren prompt-a / agentearentzako argibideak"},
    "The command/action being executed": {"es": "Comando/acción que se está ejecutando", "ca": "Ordre/acció que s'està executant", "gl": "Comando/acción que se está executando", "eu": "Exekutatzen ari den komandoa/ekintza"},
    "The skill instructions/prompt that will be injected into the agent": {"es": "Las instrucciones/prompt de la skill que se inyectarán en el agente", "ca": "Les instruccions/prompt de la skill que s'injectaran a l'agent", "gl": "As instrucións/prompt da skill que se inxectarán no axente", "eu": "Agenteari txertatuko zaizkion skill argibideak/prompt-a"},
    "These agents can use this MCP server during execution. Keep the list small to reduce accidental access to tools or data.": {
        "es": "Estos agentes pueden usar este servidor MCP durante la ejecución. Mantén la lista reducida para evitar accesos accidentales a herramientas o datos.",
        "ca": "Aquests agents poden usar aquest servidor MCP durant l'execució. Mantén la llista reduïda per evitar accessos accidentals a eines o dades.",
        "gl": "Estes axentes poden usar este servidor MCP durante a execución. Mantén a lista reducida para evitar accesos accidentais a ferramentas ou datos.",
        "eu": "Agente hauek MCP zerbitzari hau erabil dezakete exekuzioan. Mantendu zerrenda txikia tresna edo datuetara ustekabeko sarbidea murrizteko.",
    },
    "Transport": {"es": "Transporte", "ca": "Transport", "gl": "Transporte", "eu": "Garraioa"},
    "URL": {"es": "URL", "ca": "URL", "gl": "URL", "eu": "URLa"},
    "Unique machine identifier (hostname or UUID)": {"es": "Identificador único de máquina (hostname o UUID)", "ca": "Identificador únic de màquina (hostname o UUID)", "gl": "Identificador único de máquina (hostname ou UUID)", "eu": "Makina identifikatzaile bakarra (hostname edo UUID)"},
    "Unread": {"es": "No leído", "ca": "No llegit", "gl": "Non lido", "eu": "Irakurri gabe"},
    "Use this tab to see what this runtime is currently running or has recently completed.": {"es": "Usa esta pestaña para ver qué está ejecutando este runtime o qué ha completado recientemente.", "ca": "Usa aquesta pestanya per veure què està executant aquest runtime o què ha completat recentment.", "gl": "Usa esta pestana para ver que está executando este runtime ou que completou recentemente.", "eu": "Erabili fitxa hau runtime honek une honetan zer exekutatzen duen edo berriki zer osatu duen ikusteko."},
    "Version": {"es": "Versión", "ca": "Versió", "gl": "Versión", "eu": "Bertsioa"},
    "Working": {"es": "Trabajando", "ca": "Treballant", "gl": "Traballando", "eu": "Lanean"},
    "Working Agents": {"es": "Agentes trabajando", "ca": "Agents treballant", "gl": "Axentes traballando", "eu": "Lanean ari diren agenteak"},
    "Write the agent's operating rules here: role, boundaries, project context, expected output format, and what it must never do without human approval. Other agents can mention this agent with its @handle.": {
        "es": "Escribe aquí las reglas operativas del agente: rol, límites, contexto del proyecto, formato de salida esperado y qué no debe hacer nunca sin aprobación humana. Otros agentes pueden mencionar este agente con su @identificador.",
        "ca": "Escriu aquí les regles operatives de l'agent: rol, límits, context del projecte, format de sortida esperat i què no ha de fer mai sense aprovació humana. Altres agents poden mencionar aquest agent amb el seu @identificador.",
        "gl": "Escribe aquí as regras operativas do axente: rol, límites, contexto do proxecto, formato de saída esperado e que non debe facer nunca sen aprobación humana. Outros axentes poden mencionar este axente co seu @identificador.",
        "eu": "Idatzi hemen agentearen funtzionamendu-arauak: rola, mugak, proiektuaren testuingurua, espero den irteera formatua eta giza onarpenik gabe inoiz egin behar ez duena. Beste agenteek agente hau aipa dezakete bere @identifikatzailearekin.",
    },
    "Agent <b>%s</b> completed task: %s": {"ca": "L'agent <b>%s</b> ha completat la tasca: %s", "gl": "O axente <b>%s</b> completou a tarefa: %s", "eu": "<b>%s</b> agenteak zeregina osatu du: %s"},
    "Agent <b>%s</b> failed task: %s": {"ca": "L'agent <b>%s</b> ha fallat en la tasca: %s", "gl": "O axente <b>%s</b> fallou na tarefa: %s", "eu": "<b>%s</b> agenteak huts egin du zereginean: %s"},
    "Agent is working on this task": {"ca": "L'agent està treballant en aquesta tasca", "gl": "O axente está traballando nesta tarefa", "eu": "Agentea zeregin honetan lanean ari da"},
    "Provides a native multi-agent execution architecture inside Odoo. - Agent Runtimes: external machines (N100, Mac Mini, etc.) connected via API - AI Agents: configurable entities with instructions, skills, and runtime assignment - Agent Skills: reusable instruction packs - Agent Executions: repeatable runtime work units linked to project.task - Execution Logs: detailed command history with streaming support - Agent Chat: direct messaging between users and AI agents - Stage Mapping: configurable agent status to project stage mapping - REST API: bidirectional communication with external runtimes": {
        "ca": "Proporciona una arquitectura nativa d'execució multiagent dins d'Odoo. - Runtimes d'agents: màquines externes connectades per API - Agents d'IA: entitats configurables amb instruccions, skills i runtime assignat - Skills d'agent: paquets reutilitzables d'instruccions - Execucions d'agent: unitats de treball repetibles vinculades a project.task - Registres d'execució: historial detallat amb suport de streaming - Xat d'agent: missatgeria directa entre usuaris i agents d'IA - Mapatge d'etapes: mapatge configurable d'estat de l'agent a etapa de projecte - API REST: comunicació bidireccional amb runtimes externs",
        "gl": "Proporciona unha arquitectura nativa de execución multiagente dentro de Odoo. - Runtimes de axentes: máquinas externas conectadas por API - Axentes de IA: entidades configurables con instrucións, skills e runtime asignado - Skills de axente: paquetes reutilizables de instrucións - Execucións de axente: unidades de traballo repetibles vinculadas a project.task - Rexistros de execución: historial detallado con soporte de streaming - Chat de axente: mensaxería directa entre usuarios e axentes de IA - Mapeo de etapas: mapeo configurable do estado do axente á etapa do proxecto - API REST: comunicación bidireccional con runtimes externos",
        "eu": "Odoo barruan multiagente exekuzio arkitektura natiboa eskaintzen du. - Agente runtimeak: API bidez konektatutako kanpoko makinak - IA agenteak: argibideak, skillak eta esleitutako runtimea dituzten entitate konfiguragarriak - Agentearen skillak: argibide-pakete berrerabilgarriak - Agentearen exekuzioak: project.task-i lotutako lan-unitate errepikagarriak - Exekuzio logak: streaming euskarria duen komando-historial xehea - Agentearen txata: erabiltzaileen eta IA agenteen arteko mezularitza zuzena - Etapa mapaketa: agentearen egoeratik proiektu etapara mapaketa konfiguragarria - REST APIa: kanpoko runtimeekin bi noranzkoko komunikazioa",
    },
}
for msg, vals in MORE_EXACT.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val

FINAL_EXACT = {
    "Agent Assigned": {"ca": "Agent assignat"},
    "Agent Done": {"ca": "Agent completat"},
    "Agent Working": {"ca": "Agent treballant"},
    "Agent delegation created": {"ca": "Delegació d'agent creada"},
    "Agent delegation skipped": {"ca": "Delegació d'agent omesa"},
    "Agent execution finished": {"ca": "Execució d'agent finalitzada"},
    "Agent execution queued": {"ca": "Execució d'agent en cua"},
    "Agent executions": {"ca": "Execucions d'agent"},
    "Mentioned Agents": {"ca": "Agents mencionats"},
    "Category": {"gl": "Categoría", "eu": "Kategoria"},
    "IP Address": {"gl": "Enderezo IP", "eu": "IP helbidea"},
    "Level": {"gl": "Nivel", "eu": "Maila"},
}
for msg, vals in FINAL_EXACT.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val

QUALITY_EXACT = {
    "Agent Assigned": {"es": "Agente asignado", "ca": "Agent assignat", "gl": "Axente asignado", "eu": "Agentea esleituta"},
    "Agent Done": {"es": "Agente completado", "ca": "Agent completat", "gl": "Axente completado", "eu": "Agentea osatuta"},
    "Agent Failed": {"es": "Agente fallido", "ca": "Agent fallat", "gl": "Axente fallido", "eu": "Agenteak huts egin du"},
    "Agent Working": {"es": "Agente trabajando", "ca": "Agent treballant", "gl": "Axente traballando", "eu": "Agentea lanean"},
    "Agent Status": {"es": "Estado del agente", "ca": "Estat de l'agent", "gl": "Estado do axente", "eu": "Agentearen egoera"},
    "Agent Execution Count": {"es": "Número de ejecuciones de agente", "ca": "Nombre d'execucions d'agent", "gl": "Número de execucións de axente", "eu": "Agentearen exekuzio kopurua"},
    "Agent delegation created": {"es": "Delegación de agente creada", "ca": "Delegació d'agent creada", "gl": "Delegación de axente creada", "eu": "Agentearen delegazioa sortu da"},
    "Agent delegation skipped": {"es": "Delegación de agente omitida", "ca": "Delegació d'agent omesa", "gl": "Delegación de axente omitida", "eu": "Agentearen delegazioa saltatu da"},
    "Agent execution finished": {"es": "Ejecución de agente finalizada", "ca": "Execució d'agent finalitzada", "gl": "Execución de axente finalizada", "eu": "Agentearen exekuzioa amaitu da"},
    "Agent execution queued": {"es": "Ejecución de agente en cola", "ca": "Execució d'agent en cua", "gl": "Execución de axente en cola", "eu": "Agentearen exekuzioa ilaran"},
    "Agent executions": {"es": "Ejecuciones de agente", "ca": "Execucions d'agent", "gl": "Execucións de axente", "eu": "Agentearen exekuzioak"},
    "Latest Agent Execution": {"es": "Última ejecución de agente", "ca": "Última execució d'agent", "gl": "Última execución de axente", "eu": "Agentearen azken exekuzioa"},
    "Latest Agent Status": {"es": "Último estado del agente", "ca": "Últim estat de l'agent", "gl": "Último estado do axente", "eu": "Agentearen azken egoera"},
    "Legacy Agent Task": {"es": "Tarea legacy de agente", "ca": "Tasca legacy d'agent", "gl": "Tarefa legacy de axente", "eu": "Agentearen legacy zeregina"},
    "Legacy Max Concurrent Tasks": {"es": "Máximo de tareas legacy concurrentes", "ca": "Màxim de tasques legacy concurrents", "gl": "Máximo de tarefas legacy concorrentes", "eu": "Legacy zeregin paraleloen gehienekoa"},
    "Legacy Tasks": {"es": "Tareas legacy", "ca": "Tasques legacy", "gl": "Tarefas legacy", "eu": "Legacy zereginak"},
    "Mentioned Agents": {"es": "Agentes mencionados", "ca": "Agents mencionats", "gl": "Axentes mencionados", "eu": "Aipatutako agenteak"},
    "Queued Executions": {"es": "Ejecuciones en cola", "ca": "Execucions en cua", "gl": "Execucións en cola", "eu": "Ilarako exekuzioak"},
    "Running Executions": {"es": "Ejecuciones en curso", "ca": "Execucions en curs", "gl": "Execucións en curso", "eu": "Martxan dauden exekuzioak"},
    "Failed Executions": {"es": "Ejecuciones fallidas", "ca": "Execucions fallades", "gl": "Execucións fallidas", "eu": "Huts egindako exekuzioak"},
    "Idle Agents": {"es": "Agentes inactivos", "ca": "Agents inactius", "gl": "Axentes inactivos", "eu": "Agente inaktiboak"},
}
for msg, vals in QUALITY_EXACT.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val

PHASE9_EXACT = {
    "Chat": {"es": "Chat", "ca": "Xat", "gl": "Chat", "eu": "Txata"},
    "Chat Messages": {"es": "Mensajes de chat", "ca": "Missatges de xat", "gl": "Mensaxes de chat", "eu": "Txat mezuak"},
    "Chat executions keep the user request, runtime work, and agent replies traceable. Live notifications are published on the Odoo bus for this execution and agent.": {
        "es": "Las ejecuciones de chat mantienen trazables la petición del usuario, el trabajo del runtime y las respuestas del agente. Las notificaciones en vivo se publican en el bus de Odoo para esta ejecución y agente.",
        "ca": "Les execucions de xat mantenen traçables la petició de l'usuari, la feina del runtime i les respostes de l'agent. Les notificacions en viu es publiquen al bus d'Odoo per a aquesta execució i agent.",
        "gl": "As execucións de chat manteñen trazables a petición do usuario, o traballo do runtime e as respostas do axente. As notificacións en vivo publícanse no bus de Odoo para esta execución e axente.",
        "eu": "Txat exekuzioek erabiltzailearen eskaera, runtimearen lana eta agentearen erantzunak trazagarri mantentzen dituzte. Zuzeneko jakinarazpenak Odoo busean argitaratzen dira exekuzio eta agente honentzat.",
    },
    "Delivery State": {"es": "Estado de entrega", "ca": "Estat de lliurament", "gl": "Estado de entrega", "eu": "Bidalketa egoera"},
    "From Agents": {"es": "De agentes", "ca": "D'agents", "gl": "De axentes", "eu": "Agenteetatik"},
    "From Users": {"es": "De usuarios", "ca": "D'usuaris", "gl": "De usuarios", "eu": "Erabiltzaileetatik"},
    "Mark as Read": {"es": "Marcar como leído", "ca": "Marca com a llegit", "gl": "Marcar como lido", "eu": "Markatu irakurrita"},
    "Source": {"es": "Origen", "ca": "Origen", "gl": "Orixe", "eu": "Jatorria"},
    "Legacy Related Task": {"es": "Tarea legacy relacionada", "ca": "Tasca legacy relacionada", "gl": "Tarefa legacy relacionada", "eu": "Lotutako legacy zeregina"},
    "Related Project Task": {"es": "Tarea de proyecto relacionada", "ca": "Tasca de projecte relacionada", "gl": "Tarefa de proxecto relacionada", "eu": "Lotutako proiektu zeregina"},
    "Source Chat Message": {"es": "Mensaje de chat origen", "ca": "Missatge de xat origen", "gl": "Mensaxe de chat orixe", "eu": "Jatorrizko txat mezua"},
    "Sent": {"es": "Enviado", "ca": "Enviat", "gl": "Enviado", "eu": "Bidalia"},
    "Delivered": {"es": "Entregado", "ca": "Lliurat", "gl": "Entregado", "eu": "Entregatua"},
    "Manual": {"es": "Manual", "ca": "Manual", "gl": "Manual", "eu": "Eskuzkoa"},
}
for msg, vals in PHASE9_EXACT.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val

REPRODUCIBLE_EXACT = {
    "Category": {"es": "Categoría", "ca": "Categoria", "gl": "Categoría", "eu": "Kategoria"},
    "Group By": {"es": "Agrupar por", "ca": "Agrupa per", "gl": "Agrupar por", "eu": "Taldekatu honen arabera"},
    "IP Address": {"es": "Dirección IP", "ca": "Adreça IP", "gl": "Enderezo IP", "eu": "IP helbidea"},
    "Level": {"es": "Nivel", "ca": "Nivell", "gl": "Nivel", "eu": "Maila"},
}
for msg, vals in REPRODUCIBLE_EXACT.items():
    for lang, val in vals.items():
        CUSTOM.setdefault(lang, {})[msg] = val







def normalize(msg: str) -> str:
    return " ".join(str(msg).split())


def should_skip(msg: str) -> bool:
    if not msg or msg in SKIP_VALUES:
        return True
    if msg.startswith("%(action_"):
        return True
    if msg in {"1", "0"}:
        return True
    return False


def add(entries: dict[str, set[tuple[str, int]]], msg: str | None, path: Path, line: int = 1) -> None:
    if msg is None:
        return
    msg = normalize(msg)
    if should_skip(msg):
        return
    entries.setdefault(msg, set()).add((str(path), line))


def extract() -> dict[str, set[tuple[str, int]]]:
    entries: dict[str, set[tuple[str, int]]] = {}
    data = ast.literal_eval((ROOT / "__manifest__.py").read_text())
    for key in ("name", "summary", "description"):
        add(entries, data.get(key), ROOT / "__manifest__.py")

    for path in ROOT.rglob("*.py"):
        if "tests" in path.parts:
            continue
        source = path.read_text()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id == "_":
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    add(entries, node.args[0].value, path, node.lineno)
            for kw in node.keywords:
                if kw.arg in {"string", "help"} and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    add(entries, kw.value.value, path, node.lineno)
                if kw.arg == "selection" and isinstance(kw.value, (ast.List, ast.Tuple)):
                    for item in kw.value.elts:
                        if isinstance(item, (ast.List, ast.Tuple)) and len(item.elts) >= 2:
                            label = item.elts[1]
                            if isinstance(label, ast.Constant) and isinstance(label.value, str):
                                add(entries, label.value, path, getattr(item, "lineno", node.lineno))

    for path in ROOT.rglob("*.xml"):
        root = ET.parse(path).getroot()
        for element in root.iter():
            for attr in XML_ATTRS:
                add(entries, element.attrib.get(attr), path)
            if element.tag in XML_TEXT_TAGS and element.text and element.text.strip():
                add(entries, element.text, path)
    return dict(sorted(entries.items()))


def po_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'


def write_po_entry(lines: list[str], msgid: str, msgstr: str = "", refs: set[tuple[str, int]] | None = None) -> None:
    if refs:
        for ref, line in sorted(refs):
            lines.append(f"#: {ref}:{line}")
    lines.append(f"msgid {po_quote(msgid)}")
    lines.append(f"msgstr {po_quote(msgstr)}")
    lines.append("")


def header(lang: str | None = None) -> str:
    year = dt.datetime.now().year
    language = lang or ""
    return "\n".join([
        "# Translation of Odoo Server.",
        f"# This file contains the translation of the following modules: {ADDON}",
        f"# Copyright (C) {year}",
        "#",
        "msgid \"\"",
        "msgstr \"\"",
        f"\"Project-Id-Version: {ADDON} 18.0\\n\"",
        "\"Report-Msgid-Bugs-To: \\n\"",
        f"\"POT-Creation-Date: {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M+0000')}\\n\"",
        "\"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n\"",
        "\"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n\"",
        "\"Language-Team: \\n\"",
        f"\"Language: {language}\\n\"",
        "\"MIME-Version: 1.0\\n\"",
        "\"Content-Type: text/plain; charset=UTF-8\\n\"",
        "\"Content-Transfer-Encoding: 8bit\\n\"",
        "\"Plural-Forms: nplurals=2; plural=(n != 1);\\n\"",
        "",
    ])


def parse_base_po(lang: str) -> dict[str, str]:
    for base in ODOO_BASE_I18N:
        path = base / f"{lang}.po"
        if not path.exists():
            continue
        return parse_po(path)
    return {}


def parse_po(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    msgid = None
    msgstr = None
    current = None
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if line.startswith("msgid "):
            if msgid is not None and msgstr:
                result[msgid] = msgstr
            msgid = ast.literal_eval(line[6:])
            msgstr = ""
            current = "msgid"
        elif line.startswith("msgstr "):
            msgstr = ast.literal_eval(line[7:])
            current = "msgstr"
        elif line.startswith('"') and current:
            value = ast.literal_eval(line)
            if current == "msgid" and msgid is not None:
                msgid += value
            elif current == "msgstr" and msgstr is not None:
                msgstr += value
        elif not line:
            if msgid is not None and msgstr:
                result[msgid] = msgstr
            msgid = msgstr = None
            current = None
    if msgid is not None and msgstr:
        result[msgid] = msgstr
    return result


def translate(msgid: str, lang: str, base: dict[str, str]) -> str:
    if msgid in CUSTOM.get(lang, {}):
        return CUSTOM[lang][msgid]
    if msgid in base and base[msgid]:
        return base[msgid]
    terms = TERM_MAP[lang]
    if msgid in terms:
        return terms[msgid]
    # Conservative composition for short labels such as "Agent Status".
    if len(msgid.split()) <= 4 and not any(ch in msgid for ch in "<>%"):
        translated = msgid
        for source in sorted(terms, key=len, reverse=True):
            translated = re.sub(rf"\b{re.escape(source)}\b", terms[source], translated)
        if translated != msgid:
            return translated
    return ""


def main() -> None:
    I18N.mkdir(exist_ok=True)
    entries = extract()

    pot_lines = [header(None)]
    for msgid, refs in entries.items():
        write_po_entry(pot_lines, msgid, refs=refs)
    (I18N / f"{ADDON}.pot").write_text("\n".join(pot_lines))

    for lang in LANGS:
        base = parse_base_po(lang)
        lines = [header(lang)]
        missing = 0
        for msgid, refs in entries.items():
            msgstr = translate(msgid, lang, base)
            if not msgstr:
                missing += 1
            write_po_entry(lines, msgid, msgstr=msgstr, refs=refs)
        (I18N / f"{lang}.po").write_text("\n".join(lines))
        print(f"{lang}: {len(entries) - missing}/{len(entries)} translated")
    ca_es = (I18N / "ca.po").read_text().replace(
        '"Language: ca\\n"',
        '"Language: ca_ES\\n"',
    )
    (I18N / "ca_ES.po").write_text(ca_es)
    print("ca_ES: copied from ca")
    print(f"template: {len(entries)} terms")


if __name__ == "__main__":
    main()
