
import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Mining Report Pro - Control de Turno",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Bloque HTML optimizado sin conflictos de comillas en Python
html_code = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Informes Técnicos - Industrial Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- html2pdf.js para exportación a PDF de múltiples páginas -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <!-- Alpine.js para interactividad reactiva -->
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
        @media print {
            .no-print { display: none !important; }
            body { background: white !important; margin: 0; padding: 0; }
            .print-page { box-shadow: none !important; border: none !important; width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 10mm !important; page-break-after: always; }
            .avoid-break { page-break-inside: avoid !important; break-inside: avoid !important; }
            .force-page-break { page-break-before: always !important; break-before: page !important; }
        }
        .pdf-render-mode { width: 794px !important; box-sizing: border-box !important; }
        .avoid-break { page-break-inside: avoid !important; break-inside: avoid !important; }
        .force-page-break { page-break-before: always !important; break-before: page !important; }
    </style>
</head>
<body class="bg-industrialBg text-slate-800 antialiased min-h-screen flex flex-col justify-between" x-data="reportApp()">

    <!-- Header Principal -->
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
                    <i class="fa-solid fa-file-pdf"></i><span>Descargar PDF</span>
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
        
        <!-- VISTA 1: EDITOR DE DATOS -->
        <div x-show="activeTab === 'editor'" class="no-print space-y-6">
            
            <!-- Datos de Empresa y Dotación -->
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
                    <!-- DOTACIÓN / PERSONAL ASIGNADO -->
                    <div class="sm:col-span-2 lg:col-span-3 bg-teal-50/60 border border-teal-200 p-3 rounded-lg">
                        <label class="block text-xs font-bold text-corporateDark mb-1 flex items-center space-x-1.5">
                            <i class="fa-solid fa-users text-corporate"></i>
                            <span>Dotación Total / Personal Asignado en Turno</span>
                        </label>
                        <input type="text" x-model="header.workforce" placeholder="Ej: 12 Personas (2 Operadores, 1 Supervisor, 9 Aseo)" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                </div>
                <div class="mt-4">
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Nota General u Observación Crítica</label>
                    <input type="text" x-model="header.note" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                </div>
            </div>

            <!-- Equipos y Maquinaria -->
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
                                    <td class="p-1.5"><input type="text" x-model="eq.nextMaint" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5"><input type="text" x-model="eq.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5 text-center"><button @click="removeEquipment(index)" class="text-red-500 hover:text-red-700 p-1"><i class="fa-solid fa-trash-can text-xs"></i></button></td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Actividades Realizadas -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-list-check text-corporate"></i>
                        <span>3. Actividades Realizadas</span>
                    </h2>
                    <button @click="addActivity()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium">
                        <i class="fa-solid fa-plus"></i> Añadir Actividad
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs min-w-[550px]">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-[11px] uppercase font-semibold">
                                <th class="p-2.5 w-8 text-center">#</th>
                                <th class="p-2.5 w-40">Lugar Específico</th>
                                <th class="p-2.5">Actividad Realizada</th>
                                <th class="p-2.5 w-24 text-center">% Avance</th>
                                <th class="p-2.5 text-center w-12">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(act, index) in activityList" :key="index">
                                <tr>
                                    <td class="p-1.5 text-center font-semibold text-xs text-slate-500" x-text="index + 1"></td>
                                    <td class="p-1.5"><input type="text" x-model="act.location" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5"><input type="text" x-model="act.description" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5 text-center"><input type="number" min="0" max="100" x-model="act.progress" class="w-16 border border-slate-200 rounded p-1.5 text-xs text-center"></td>
                                    <td class="p-1.5 text-center"><button @click="removeActivity(index)" class="text-red-500 hover:text-red-700 p-1"><i class="fa-solid fa-trash-can text-xs"></i></button></td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Estado de Instalaciones -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-house-chimney text-corporate"></i>
                        <span>4. Estado de Instalaciones de Faena / Sala de Cambio</span>
                    </h2>
                    <button @click="addFacility()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium">
                        <i class="fa-solid fa-plus"></i> Añadir Elemento
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs min-w-[500px]">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-[11px] uppercase font-semibold">
                                <th class="p-2.5 w-48">Elemento / Área</th>
                                <th class="p-2.5 w-36">Estado</th>
                                <th class="p-2.5">Observaciones</th>
                                <th class="p-2.5 text-center w-12">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(fac, index) in facilityList" :key="index">
                                <tr>
                                    <td class="p-1.5"><input type="text" x-model="fac.element" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5">
                                        <select x-model="fac.status" class="w-full border border-slate-200 rounded p-1.5 text-xs bg-white font-medium">
                                            <option value="BUENO">BUENO / OPERATIVO</option>
                                            <option value="REGULAR">REGULAR</option>
                                            <option value="MALO">MALO / DEFECTUOSO</option>
                                        </select>
                                    </td>
                                    <td class="p-1.5"><input type="text" x-model="fac.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs"></td>
                                    <td class="p-1.5 text-center"><button @click="removeFacility(index)" class="text-red-500 hover:text-red-700 p-1"><i class="fa-solid fa-trash-can text-xs"></i></button></td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Anexo Fotográfico -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-100">
                    <div>
                        <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                            <i class="fa-solid fa-camera-retro text-corporate"></i>
                            <span>5. Anexo Fotográfico (Antes y Después)</span>
                        </h2>
                        <p class="text-[11px] text-slate-500 mt-0.5">Se colocará automáticamente en la última hoja del informe sin cortar las fotos.</p>
                    </div>
                    <button @click="addPhotoPair()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium">
                        <i class="fa-solid fa-plus"></i> Nueva Comparativa
                    </button>
                </div>
                
                <div class="space-y-6">
                    <template x-for="(pair, index) in photoPairs" :key="index">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 sm:p-4 relative">
                            <div class="flex justify-between items-center mb-3">
                                <span class="text-xs font-bold text-petroleum uppercase bg-slate-200 px-2 py-0.5 rounded">Comparativa N° <span x-text="index + 1"></span></span>
                                <button @click="removePhotoPair(index)" class="text-red-500 hover:text-red-700 text-xs font-medium"><i class="fa-solid fa-trash-can"></i> Eliminar</button>
                            </div>
                            
                            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
                                <div>
                                    <label class="block text-[11px] font-semibold text-slate-600 mb-1">Ubicación / Sector</label>
                                    <input type="text" x-model="pair.location" placeholder="Ej: CT 135 C" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                                <div class="sm:col-span-2">
                                    <label class="block text-[11px] font-semibold text-slate-600 mb-1">Descripción de la tarea ejecutada</label>
                                    <input type="text" x-model="pair.description" placeholder="Ej: Limpieza manual de pasillo" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                            </div>

                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-200">
                                <!-- ANTES -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-amber-700 mb-1.5"><i class="fa-solid fa-clock-rotate-left"></i> FOTO ANTES</label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-20 h-20 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.beforeImg"><img :src="pair.beforeImg" class="w-full h-full object-cover"></template>
                                            <template x-if="!pair.beforeImg"><i class="fa-solid fa-image text-slate-300 text-xl"></i></template>
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'beforeImg')" class="w-full text-[10px] text-slate-500">
                                            <input type="text" x-model="pair.beforeNote" placeholder="Observación estado previo" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>
                                <!-- DESPUÉS -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-emerald-700 mb-1.5"><i class="fa-solid fa-circle-check"></i> FOTO DESPUÉS</label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-20 h-20 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.afterImg"><img :src="pair.afterImg" class="w-full h-full object-cover"></template>
                                            <template x-if="!pair.afterImg"><i class="fa-solid fa-image text-slate-300 text-xl"></i></template>
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'afterImg')" class="w-full text-[10px] text-slate-500">
                                            <input type="text" x-model="pair.afterNote" placeholder="Observación resultado final" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>

        <!-- VISTA 2: PREVIEW E IMPRESIÓN PDF -->
        <div class="flex justify-center w-full overflow-x-auto">
            <div id="full-report-container" class="bg-white p-6 shadow-2xl border border-slate-300 text-slate-900 text-xs my-2 print-page" style="width: 210mm; min-h: 297mm; box-sizing: border-box;">
                
                <!-- PÁGINA 1 -->
                <div class="flex flex-col justify-between min-h-[265mm]">
                    <div>
                        <div class="border-2 border-slate-800 mb-3 grid grid-cols-12 text-center">
                            <div class="col-span-4 border-r-2 border-slate-800 p-2 flex items-center justify-center bg-slate-50">
                                <div>
                                    <span class="font-extrabold text-xs sm:text-sm tracking-wider text-slate-900 uppercase block" x-text="header.company"></span>
                                    <span class="text-[8px] text-slate-500 font-bold">SISTEMA INTEGRADO DE GESTIÓN</span>
                                </div>
                            </div>
                            <div class="col-span-6 border-r-2 border-slate-800 p-2 flex items-center justify-center bg-white">
                                <span class="font-bold text-xs sm:text-sm tracking-wide uppercase" x-text="header.title"></span>
                            </div>
                            <div class="col-span-2 p-2 flex flex-col justify-center items-center text-[9px] font-bold bg-slate-50">
                                <span>PÁG. 1 DE 2</span>
                            </div>
                        </div>

                        <div class="border border-slate-800 mb-3 text-[10px]">
                            <div class="bg-slate-200 font-bold px-3 py-1 border-b border-slate-800 text-slate-800 uppercase tracking-wide" x-text="header.area"></div>
                            <div class="grid grid-cols-2 border-b border-slate-300">
                                <div class="p-1.5 px-3 border-r border-slate-300 font-semibold">TURNO: <span class="font-normal uppercase" x-text="header.shift"></span></div>
                                <div class="p-1.5 px-3 font-semibold">FECHA: <span class="font-normal" x-text="header.date"></span></div>
                            </div>
                            <div class="p-1.5 px-3 border-b border-slate-300 font-semibold bg-slate-50">
                                SUPERVISOR A CARGO: <span class="font-normal uppercase" x-text="header.supervisor"></span>
                            </div>
                            <div class="p-1.5 px-3 font-semibold bg-teal-50/70 text-slate-900">
                                DOTACIÓN / PERSONAL ASIGNADO: <span class="font-normal" x-text="header.workforce || 'No especificada'"></span>
                            </div>
                        </div>

                        <!-- 1. Equipos -->
                        <div class="mb-3 avoid-break">
                            <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[10px] uppercase tracking-wide mb-1">1. Equipos y Maquinaria en Turno</div>
                            <table class="w-full border-collapse border border-slate-400 text-[9px]">
                                <thead>
                                    <tr class="bg-slate-100 text-slate-800 font-bold">
                                        <th class="border border-slate-400 p-1 text-left w-1/4">EQUIPOS</th>
                                        <th class="border border-slate-400 p-1 text-center w-24">COMBUSTIBLE</th>
                                        <th class="border border-slate-400 p-1 text-center w-24">HORÓMETROS / KM</th>
                                        <th class="border border-slate-400 p-1 text-center w-20">PRÓX. MANT.</th>
                                        <th class="border border-slate-400 p-1 text-left">OBSERVACIONES</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template x-for="eq in equipmentList" :key="eq.name">
                                        <tr>
                                            <td class="border border-slate-300 p-1 font-semibold" x-text="eq.name"></td>
                                            <td class="border border-slate-300 p-1 text-center">
                                                <div class="flex justify-center space-x-1 text-[8px]">
                                                    <span :class="eq.fuel === '1/4' ? 'font-bold bg-slate-300 px-0.5 rounded' : 'text-slate-400'">1/4</span>
                                                    <span :class="eq.fuel === '1/2' ? 'font-bold bg-slate-300 px-0.5 rounded' : 'text-slate-400'">1/2</span>
                                                    <span :class="eq.fuel === '3/4' ? 'font-bold bg-slate-300 px-0.5 rounded' : 'text-slate-400'">3/4</span>
                                                    <span :class="eq.fuel === 'Full' ? 'font-bold bg-slate-300 px-0.5 rounded' : 'text-slate-400'">Full</span>
                                                </div>
                                            </td>
                                            <td class="border border-slate-300 p-1 text-center" x-text="eq.horometer"></td>
                                            <td class="border border-slate-300 p-1 text-center" x-text="eq.nextMaint"></td>
                                            <td class="border border-slate-300 p-1" x-text="eq.obs"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <div class="bg-amber-50 border border-amber-300 text-amber-900 font-bold px-3 py-1 text-[9px] mb-3 avoid-break">
                            NOTA: <span class="font-normal" x-text="header.note"></span>
                        </div>

                        <!-- 2. Actividades -->
                        <div class="mb-3 avoid-break">
                            <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[10px] uppercase tracking-wide mb-1">2. Actividades Realizadas</div>
                            <table class="w-full border-collapse border border-slate-400 text-[9px]">
                                <thead>
                                    <tr class="bg-slate-100 text-slate-800 font-bold">
                                        <th class="border border-slate-400 p-1 text-center w-6">#</th>
                                        <th class="border border-slate-400 p-1 text-left w-32">LUGAR ESPECÍFICO</th>
                                        <th class="border border-slate-400 p-1 text-left">ACTIVIDAD REALIZADA</th>
                                        <th class="border border-slate-400 p-1 text-center w-16">% AVANCE</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template x-for="(act, index) in activityList" :key="index">
                                        <tr>
                                            <td class="border border-slate-300 p-1 text-center font-bold" x-text="index + 1"></td>
                                            <td class="border border-slate-300 p-1 font-semibold" x-text="act.location"></td>
                                            <td class="border border-slate-300 p-1" x-text="act.description"></td>
                                            <td class="border border-slate-300 p-1 text-center font-bold" x-text="act.progress + '%'"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                        <!-- 3. Instalaciones -->
                        <div class="mb-3 avoid-break">
                            <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[10px] uppercase tracking-wide mb-1">3. Estado de Instalaciones de Faena / Sala de Cambio</div>
                            <table class="w-full border-collapse border border-slate-400 text-[9px]">
                                <thead>
                                    <tr class="bg-slate-100 text-slate-800 font-bold">
                                        <th class="border border-slate-400 p-1 text-left w-1/3">ELEMENTOS</th>
                                        <th class="border border-slate-400 p-1 text-center w-24">ESTADO</th>
                                        <th class="border border-slate-400 p-1 text-left">OBSERVACIONES</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <template x-for="fac in facilityList" :key="fac.element">
                                        <tr>
                                            <td class="border border-slate-300 p-1 font-semibold" x-text="fac.element"></td>
                                            <td class="border border-slate-300 p-1 text-center font-bold" :class="fac.status === 'BUENO' ? 'text-emerald-700' : 'text-red-700'" x-text="fac.status"></td>
                                            <td class="border border-slate-300 p-1" x-text="fac.obs"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="text-[8px] text-slate-500 border-t border-slate-300 pt-1 flex justify-between mt-2">
                        <span x-text="header.company + ' - Control Operacional de Turno'"></span>
                        <span>Documento Digital Generado Oficial</span>
                    </div>
                </div>

                <div class="force-page-break pt-4"></div>

                <!-- PÁGINA 2: ANEXO FOTOGRÁFICO -->
                <div class="flex flex-col justify-between min-h-[265mm]">
                    <div>
                        <div class="border-2 border-slate-800 mb-4 grid grid-cols-12 bg-slate-50 text-center">
                            <div class="col-span-9 p-2 border-r-2 border-slate-800 text-left">
                                <span class="font-extrabold text-xs tracking-wider text-slate-900 uppercase block" x-text="header.company"></span>
                                <span class="font-bold text-[10px] text-corporate uppercase">ANEXO FOTOGRÁFICO - REGISTRO DE TRABAJOS (ANTES / DESPUÉS)</span>
                            </div>
                            <div class="col-span-3 p-2 flex flex-col justify-center items-center text-[9px] font-bold">
                                <span>PÁG. 2 DE 2</span>
                                <span class="text-[8px] text-slate-500 font-normal" x-text="header.date"></span>
                            </div>
                        </div>

                        <div class="space-y-4">
                            <template x-for="(pair, index) in photoPairs" :key="index">
                                <div class="border border-slate-400 rounded-lg p-2.5 bg-slate-50/50 avoid-break">
                                    <div class="flex justify-between items-center border-b border-slate-300 pb-1 mb-2">
                                        <span class="font-bold text-slate-800 text-[10px]">COMPARATIVA N° <span x-text="index + 1"></span> - <span x-text="pair.location"></span></span>
                                        <span class="text-slate-600 text-[9px]" x-text="pair.description"></span>
                                    </div>
                                    <div class="grid grid-cols-2 gap-3">
                                        <div class="bg-white p-2 rounded border border-slate-300 text-center">
                                            <div class="font-bold text-amber-700 text-[9px] mb-1"><i class="fa-solid fa-clock-rotate-left"></i> ANTES DE LA TAREA</div>
                                            <div class="h-36 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1">
                                                <template x-if="pair.beforeImg"><img :src="pair.beforeImg" class="w-full h-full object-cover"></template>
                                                <template x-if="!pair.beforeImg"><span class="text-slate-400 italic text-[9px]">Sin foto</span></template>
                                            </div>
                                            <p class="text-[9px] text-slate-600 italic truncate" x-text="pair.beforeNote || 'Estado previo'"></p>
                                        </div>
                                        <div class="bg-white p-2 rounded border border-slate-300 text-center">
                                            <div class="font-bold text-emerald-700 text-[9px] mb-1"><i class="fa-solid fa-circle-check"></i> DESPUÉS DE LA TAREA</div>
                                            <div class="h-36 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1">
                                                <template x-if="pair.afterImg"><img :src="pair.afterImg" class="w-full h-full object-cover"></template>
                                                <template x-if="!pair.afterImg"><span class="text-slate-400 italic text-[9px]">Sin foto</span></template>
                                            </div>
                                            <p class="text-[9px] text-slate-600 italic truncate" x-text="pair.afterNote || 'Resultado final'"></p>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <div class="text-[8px] text-slate-500 border-t border-slate-300 pt-1 flex justify-between mt-4">
                        <span x-text="header.company + ' - Registro Fotográfico de Evidencia'"></span>
                        <span>Fin del Informe Técnico</span>
                    </div>
                </div>

            </div>
        </div>

    </main>

    <script>
        function reportApp() {
            return {
                activeTab: 'editor',
                notification: false,
                notificationText: '',
                
                header: {
                    company: 'CODELCO - DIVISIÓN TENIENTE',
                    title: 'INFORME ENTREGA DE TURNO DIARIO',
                    area: 'ÁREA CHANCADO SECUNDARIO - TERCIARIO',
                    shift: 'TURNO: B, NOCHE',
                    date: new Date().toISOString().split('T')[0],
                    supervisor: 'HERNAN GONZALO TRONCOSO OÑATE',
                    workforce: '14 Personas (4 Operadores Aspirador, 2 Cargador, 7 Aseo, 1 APR)',
                    note: 'REVISAR AIRE ACONDICIONADO DE SALA CAMBIO, OFICINA Y SALA REUNIONES'
                },

                equipmentList: [
                    { name: 'Camión aspirador 12', fuel: '3/4', horometer: '5853 / 5861', nextMaint: '4270', obs: 'Equipo operativo, recarga combustible.' },
                    { name: 'Camión aspirador 34', fuel: 'Full', horometer: '12693 / 12670', nextMaint: '12740', obs: 'Equipo Operativo, combustible 140 LTS.' },
                    { name: 'Mini cargador 450', fuel: '1/2', horometer: '2212.6 / 2214.6', nextMaint: '2500.0', obs: 'Equipo operativo.' },
                    { name: 'Camioneta VPBW 16', fuel: 'Full', horometer: '9633.1 / 9', nextMaint: '10.000', obs: 'Equipo operativo.' }
                ],

                activityList: [
                    { location: 'CT 135 C', description: 'LIMPIEZA MANUAL SECTOR PASILLO IZQUIERDO', progress: 100 },
                    { location: 'CH 2°, 3°', description: 'HUMECTACION DE CAMINOS 2 VECES (APOYO PRIMARIO)', progress: 100 },
                    { location: 'SILICA', description: 'LIMPIEZA MANUAL SECTOR PARRILLA Y ACCESO', progress: 100 }
                ],

                facilityList: [
                    { element: 'CASILLEROS', status: 'BUENO', obs: 'OPERATIVO' },
                    { element: 'DUCHAS', status: 'BUENO', obs: 'OPERATIVO' },
                    { element: 'BAÑOS (WC)', status: 'BUENO', obs: 'Mantener puerta cerrada' },
                    { element: 'URINARIOS', status: 'BUENO', obs: 'OK' }
                ],

                photoPairs: [
                    {
                        location: 'CT 135 C',
                        description: 'Limpieza de pasillo principal y retiro de material acumulado.',
                        beforeImg: '', beforeNote: 'Acumulación de mineral en sector pasillo.',
                        afterImg: '', afterNote: 'Sector despejado y limpio conforme a norma.'
                    }
                ],

                showNotification(msg) {
                    this.notificationText = msg;
                    this.notification = true;
                    setTimeout(() => { this.notification = false; }, 3000);
                },

                addEquipment() { this.equipmentList.push({ name: '', fuel: 'Full', horometer: '', nextMaint: '', obs: '' }); this.showNotification('Equipo agregado'); },
                removeEquipment(index) { this.equipmentList.splice(index, 1); },

                addActivity() { this.activityList.push({ location: '', description: '', progress: 100 }); this.showNotification('Actividad agregada'); },
                removeActivity(index) { this.activityList.splice(index, 1); },

                addFacility() { this.facilityList.push({ element: '', status: 'BUENO', obs: '' }); this.showNotification('Elemento agregado'); },
                removeFacility(index) { this.facilityList.splice(index, 1); },

                addPhotoPair() { this.photoPairs.push({ location: '', description: '', beforeImg: '', beforeNote: '', afterImg: '', afterNote: '' }); this.showNotification('Comparativa agregada'); },
                removePhotoPair(index) { this.photoPairs.splice(index, 1); },

                handleImageUpload(event, index, field) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            this.photoPairs[index][field] = e.target.result;
                            this.showNotification('Fotografía cargada correctamente');
                        };
                        reader.readAsDataURL(file);
                    }
                },

                exportPDF() {
                    this.showNotification('Generando PDF completo de alta calidad...');
                    const element = document.getElementById('full-report-container');
                    const originalClass = element.className;
                    element.classList.add('pdf-render-mode');
