
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mining Report Pro - Control de Turno",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Informes Técnicos - Industrial Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        petroleum: '#0f172a',
                        corporate: '#0d9488',
                        corporateDark: '#0f766e',
                        industrialBg: '#f8fafc'
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        
        /* Estilos de Impresión Nativa (PDF Perfecto en Celular y PC) */
        @media print {
            body { background: white !important; margin: 0 !important; padding: 0 !important; }
            .no-print { display: none !important; }
            .page-a4 {
                box-shadow: none !important;
                border: none !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 10mm !important;
                page-break-after: always;
            }
            .force-page-break {
                page-break-before: always !important;
                break-before: page !important;
            }
        }

        .page-a4 {
            width: 210mm;
            min-height: 297mm;
            padding: 10mm;
            margin: 0 auto;
            background: white;
            box-sizing: border-box;
        }

        .avoid-break {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }

        .force-page-break {
            page-break-before: always !important;
            break-before: page !important;
        }
    </style>
</head>
<body class="bg-industrialBg text-slate-800 antialiased min-h-screen flex flex-col justify-between" x-data="reportApp()">

    <!-- Header Principal (No se imprime) -->
    <header class="no-print bg-petroleum text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
            <div class="flex items-center space-x-3">
                <div class="bg-corporate p-2.5 rounded-lg text-white shadow">
                    <i class="fa-solid fa-industry text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-base sm:text-lg tracking-wide">MINING REPORT PRO</h1>
                    <p class="text-[11px] text-slate-400">Sistema de Información de Faena y Anexos</p>
                </div>
            </div>
            <div class="flex items-center space-x-2 w-full sm:w-auto justify-end">
                <button @click="activeTab = 'editor'" :class="activeTab === 'editor' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2 rounded-lg text-xs font-medium transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-pen-to-square"></i><span>Formulario</span>
                </button>
                <button @click="activeTab = 'preview'" :class="activeTab === 'preview' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2 rounded-lg text-xs font-medium transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-eye"></i><span>Ver Previa</span>
                </button>
                <button @click="exportPDF()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-xs font-semibold transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-file-pdf"></i><span>Guardar / Imprimir PDF</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Notificación flotante -->
    <div x-show="notification" x-transition class="no-print fixed bottom-5 right-5 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center space-x-3 border-l-4 border-corporate">
        <i class="fa-solid fa-circle-check text-corporate text-lg"></i>
        <span class="text-xs sm:text-sm font-medium" x-text="notificationText"></span>
    </div>

    <main class="max-w-7xl mx-auto px-2 sm:px-4 py-6 w-full flex-grow">
        
        <!-- VISTA 1: FORMULARIO (No se imprime) -->
        <div x-show="activeTab === 'editor'" class="no-print space-y-6">
            
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-building text-corporate"></i>
                        <span>1. Datos de Empresa, Faena y Dotación</span>
                    </h2>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Nombre de la Empresa</label>
                        <input type="text" x-model="header.company" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Título del Informe</label>
                        <input type="text" x-model="header.title" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Área / Sección de Faena</label>
                        <input type="text" x-model="header.area" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Turno Operativo</label>
                        <input type="text" x-model="header.shift" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Fecha</label>
                        <input type="date" x-model="header.date" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Supervisor / Responsable</label>
                        <input type="text" x-model="header.supervisor" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div class="sm:col-span-2 lg:col-span-3 bg-teal-50/60 border border-teal-200 p-3 rounded-lg">
                        <label class="block text-xs font-bold text-corporateDark mb-1 flex items-center space-x-1.5">
                            <i class="fa-solid fa-users text-corporate"></i>
                            <span>Dotación Total / Personal Asignado en Turno</span>
                        </label>
                        <input type="text" x-model="header.workforce" placeholder="Ej: 14 Personas (4 Operadores, 2 Cargador, 7 Aseo, 1 APR)" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                </div>
                <div class="mt-4">
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Nota General u Observación Crítica</label>
                    <input type="text" x-model="header.note" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                </div>
            </div>

            <!-- 2. Equipos -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-truck-monster text-corporate"></i>
                        <span>2. Registro de Equipos y Maquinaria</span>
                    </h2>
                    <button @click="addEquipment()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium">
                        <i class="fa-solid fa-plus"></i> Añadir Equipo
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs min-w-[600px]">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-[11px] uppercase font-semibold">
                                <th class="p-2.5">Equipo</th>
                                <th class="p-2.5 text-center w-28">Combustible</th>
                                <th class="p-2.5 w-32">Horómetro / KM</th>
                                <th class="p-2.5 w-32">Próx. Mantención</th>
                                <th class="p-2.5">Observaciones</th>
                                <th class="p-2.5 text-center w-12">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(eq, index) in equipmentList" :key="index">
                                <tr>
                                    <td class="p-1.5"><input type="text" x-model="eq.name" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5 text-center">
                                        <select x-model="eq.fuel" class="w-full border border-slate-200 rounded p-1.5 text-xs bg-white">
                                            <option value="1/4">1/4</option><option value="1/2">1/2</option><option value="3/4">3/4</option><option value="Full">Full</option>
                                        </select>
                                    </td>
                                    <td class="p-1.5"><input type="text" x-model="eq.horometer" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5"><input type="text" x-model="eq.nextMaint" class="w-full border border-slate-
