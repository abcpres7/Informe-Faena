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
            body { background: white; }
            .no-print { display: none !important; }
        }
    </style>
</head>
<body class="bg-industrialBg text-slate-800 antialiased" x-data="reportApp()">

    <!-- Header Principal (No imprime) -->
    <header class="no-print bg-petroleum text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="bg-corporate p-2.5 rounded-lg text-white shadow">
                    <i class="fa-solid fa-industry text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-wide">MINING & FAENA REPORT PRO</h1>
                    <p class="text-xs text-slate-400">Sistema de Generación de Informes Técnicos y Anexos Fotográficos</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button @click="activeTab = 'editor'" :class="activeTab === 'editor' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-4 py-2 rounded-lg text-sm font-medium transition shadow flex items-center space-x-2">
                    <i class="fa-solid fa-pen-to-square"></i>
                    <span>Editar Datos</span>
                </button>
                <button @click="activeTab = 'preview'" :class="activeTab === 'preview' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-4 py-2 rounded-lg text-sm font-medium transition shadow flex items-center space-x-2">
                    <i class="fa-solid fa-file-pdf"></i>
                    <span>Vista Previa PDF</span>
                </button>
                <button @click="exportPDF()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-lg text-sm font-semibold transition shadow flex items-center space-x-2">
                    <i class="fa-solid fa-download"></i>
                    <span>Exportar PDF</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Notificación flotante de éxito -->
    <div x-show="notification" x-transition class="no-print fixed bottom-5 right-5 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center space-x-3 border-l-4 border-corporate">
        <i class="fa-solid fa-circle-check text-corporate text-lg"></i>
        <span class="text-sm font-medium" x-text="notificationText"></span>
    </div>

    <main class="max-w-7xl mx-auto px-4 py-6">
        
        <!-- VISTA 1: EDITOR DE DATOS (FORMULARIO) -->
        <div x-show="activeTab === 'editor'" class="no-print space-y-6">
            
            <!-- Tarjeta 1: Cabecera General -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                    <h2 class="text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-building text-corporate"></i>
                        <span>1. Configuración de Cabecera y Empresa</span>
                    </h2>
                    <span class="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-md font-medium">Formato Corporativo</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Empresa / Cliente</label>
                        <input type="text" x-model="header.company" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Título del Informe</label>
                        <input type="text" x-model="header.title" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Área / Sección</label>
                        <input type="text" x-model="header.area" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Turno</label>
                        <input type="text" x-model="header.shift" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Fecha</label>
                        <input type="date" x-model="header.date" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Supervisor / Responsable</label>
                        <input type="text" x-model="header.supervisor" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                </div>
                <div class="mt-4">
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Nota General / Advertencia</label>
                    <input type="text" x-model="header.note" class="w-full text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                </div>
            </div>

            <!-- Tarjeta 2: Equipos y Maquinaria -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                    <h2 class="text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-truck-monster text-corporate"></i>
                        <span>2. Registro de Equipos y Maquinaria</span>
                    </h2>
                    <button @click="addEquipment()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Agregar Equipo</span>
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-xs uppercase font-semibold">
                                <th class="p-2.5">Equipo</th>
                                <th class="p-2.5 text-center">Combustible (1/4, 1/2, 3/4, Full)</th>
                                <th class="p-2.5">Horómetros / Kilometraje</th>
                                <th class="p-2.5">Próxima Mantención</th>
                                <th class="p-2.5">Observaciones</th>
                                <th class="p-2.5 text-center">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(eq, index) in equipmentList" :key="index">
                                <tr>
                                    <td class="p-2">
                                        <input type="text" x-model="eq.name" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2 text-center">
                                        <select x-model="eq.fuel" class="border border-slate-200 rounded p-1.5 text-xs bg-white">
                                            <option value="1/4">1/4</option>
                                            <option value="1/2">1/2</option>
                                            <option value="3/4">3/4</option>
                                            <option value="Full">Full</option>
                                        </select>
                                    </td>
                                    <td class="p-2">
                                        <input type="text" x-model="eq.horometer" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2">
                                        <input type="text" x-model="eq.nextMaint" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2">
                                        <input type="text" x-model="eq.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2 text-center">
                                        <button @click="removeEquipment(index)" class="text-red-500 hover:text-red-700 p-1">
                                            <i class="fa-solid fa-trash-can text-xs"></i>
                                        </button>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Tarjeta 3: Actividades Realizadas -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                    <h2 class="text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-list-check text-corporate"></i>
                        <span>3. Actividades Realizadas</span>
                    </h2>
                    <button @click="addActivity()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Agregar Actividad</span>
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-xs uppercase font-semibold">
                                <th class="p-2.5 w-12 text-center">#</th>
                                <th class="p-2.5">Lugar Específico</th>
                                <th class="p-2.5">Actividad Realizada</th>
                                <th class="p-2.5 w-32 text-center">% Avance</th>
                                <th class="p-2.5 text-center w-16">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(act, index) in activityList" :key="index">
                                <tr>
                                    <td class="p-2 text-center font-semibold text-xs text-slate-500" x-text="index + 1"></td>
                                    <td class="p-2">
                                        <input type="text" x-model="act.location" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2">
                                        <input type="text" x-model="act.description" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2 text-center">
                                        <input type="number" min="0" max="100" x-model="act.progress" class="w-20 border border-slate-200 rounded p-1.5 text-xs text-center">
                                    </td>
                                    <td class="p-2 text-center">
                                        <button @click="removeActivity(index)" class="text-red-500 hover:text-red-700 p-1">
                                            <i class="fa-solid fa-trash-can text-xs"></i>
                                        </button>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Tarjeta 4: Estado de Instalaciones -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                    <h2 class="text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-house-chimney text-corporate"></i>
                        <span>4. Estado de Instalaciones de Faena / Sala de Cambio</span>
                    </h2>
                    <button @click="addFacility()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Agregar Elemento</span>
                    </button>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 text-xs uppercase font-semibold">
                                <th class="p-2.5">Elemento / Área</th>
                                <th class="p-2.5 w-40">Estado</th>
                                <th class="p-2.5">Observaciones</th>
                                <th class="p-2.5 text-center w-16">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <template x-for="(fac, index) in facilityList" :key="index">
                                <tr>
                                    <td class="p-2">
                                        <input type="text" x-model="fac.element" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2">
                                        <select x-model="fac.status" class="w-full border border-slate-200 rounded p-1.5 text-xs bg-white font-medium" :class="fac.status === 'BUENO' ? 'text-emerald-600' : (fac.status === 'REGULAR' ? 'text-amber-600' : 'text-red-600')">
                                            <option value="BUENO">BUENO / OPERATIVO</option>
                                            <option value="REGULAR">REGULAR</option>
                                            <option value="MALO">MALO / DEFECTUOSO</option>
                                        </select>
                                    </td>
                                    <td class="p-2">
                                        <input type="text" x-model="fac.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-2 text-center">
                                        <button @click="removeFacility(index)" class="text-red-500 hover:text-red-700 p-1">
                                            <i class="fa-solid fa-trash-can text-xs"></i>
                                        </button>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Tarjeta 5: Anexo Fotográfico (Antes y Después) -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                    <div>
                        <h2 class="text-base font-bold text-petroleum flex items-center space-x-2">
                            <i class="fa-solid fa-camera-retro text-corporate"></i>
                            <span>5. Anexo Fotográfico (Antes y Después)</span>
                        </h2>
                        <p class="text-xs text-slate-500 mt-0.5">Las fotos subidas se ordenarán automáticamente en el anexo de la última página del informe.</p>
                    </div>
                    <button @click="addPhotoPair()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Agregar Comparativa</span>
                    </button>
                </div>
                
                <div class="space-y-6">
                    <template x-for="(pair, index) in photoPairs" :key="index">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 relative">
                            <div class="flex justify-between items-center mb-3">
                                <span class="text-xs font-bold text-petroleum uppercase bg-slate-200 px-2.5 py-1 rounded">Comparativa N° <span x-text="index + 1"></span></span>
                                <button @click="removePhotoPair(index)" class="text-red-500 hover:text-red-700 text-xs font-medium flex items-center space-x-1">
                                    <i class="fa-solid fa-trash-can"></i><span>Eliminar Par</span>
                                </button>
                            </div>
                            
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
                                <div>
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Ubicación / Sector</label>
                                    <input type="text" x-model="pair.location" placeholder="Ej: CT 135 C" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                                <div class="md:col-span-2">
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Descripción general de la tarea</label>
                                    <input type="text" x-model="pair.description" placeholder="Ej: Limpieza manual de pasillo y retiro de material" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-slate-200">
                                <!-- ANTES -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-amber-700 mb-1.5 flex items-center space-x-1">
                                        <i class="fa-solid fa-clock-rotate-left"></i><span>FOTO ANTES</span>
                                    </label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-24 h-24 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.beforeImg">
                                                <img :src="pair.beforeImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.beforeImg">
                                                <i class="fa-solid fa-image text-slate-300 text-2xl"></i>
                                            </template>
                                        </div>
                                        <div class="flex-1">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'beforeImg')" class="w-full text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100">
                                            <input type="text" x-model="pair.beforeNote" placeholder="Nota foto antes (opcional)" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>

                                <!-- DESPUÉS -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-emerald-700 mb-1.5 flex items-center space-x-1">
                                        <i class="fa-solid fa-circle-check"></i><span>FOTO DESPUÉS</span>
                                    </label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-24 h-24 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.afterImg">
                                                <img :src="pair.afterImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.afterImg">
                                                <i class="fa-solid fa-image text-slate-300 text-2xl"></i>
                                            </template>
                                        </div>
                                        <div class="flex-1">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'afterImg')" class="w-full text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100">
                                            <input type="text" x-model="pair.afterNote" placeholder="Nota foto después (opcional)" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                    <template x-if="photoPairs.length === 0">
                        <div class="text-center py-8 text-slate-400 text-xs italic bg-slate-50 rounded-xl border border-dashed border-slate-200">
                            No hay registros fotográficos agregados. Haga clic en "Agregar Comparativa" para incluir anexos.
                        </div>
                    </template>
                </div>
            </div>

        </div>

        <!-- VISTA 2: VISTA PREVIA DEL DOCUMENTO PDF (Formato Oficial Codelco / Aramark) -->
        <div class="mt-6 flex justify-center">
            <div id="report-document" class="bg-white w-[210mm] min-h-[297mm] p-[15mm] shadow-2xl border border-slate-200 text-slate-900 text-xs relative flex flex-col justify-between">
                
                <!-- Contenido Principal de Páginas -->
                <div>
                    <!-- Cabecera Oficial del Informe -->
                    <div class="border-2 border-slate-800 mb-4 grid grid-cols-12">
                        <div class="col-span-4 border-r-2 border-slate-800 p-2 flex items-center justify-center bg-slate-50">
                            <div class="text-center">
                                <span class="font-extrabold text-sm tracking-widest text-slate-900 uppercase" x-text="header.company"></span>
                                <div class="text-[9px] text-slate-500 font-semibold mt-0.5">SISTEMA DE GESTIÓN INTEGRADA</div>
                            </div>
                        </div>
                        <div class="col-span-6 border-r-2 border-slate-800 p-2 flex items-center justify-center">
                            <span class="font-bold text-sm tracking-wider uppercase text-center" x-text="header.title"></span>
                        </div>
                        <div class="col-span-2 p-2 flex flex-col justify-center items-center text-[10px] font-bold bg-slate-50">
                            <span>Página 1 de 2</span>
                        </div>
                    </div>

                    <!-- Datos Generales e Identificación -->
                    <div class="border border-slate-800 mb-4 text-[11px]">
                        <div class="bg-slate-200 font-bold px-3 py-1 border-b border-slate-800 text-slate-800 uppercase tracking-wide" x-text="header.area"></div>
                        <div class="grid grid-cols-2 border-b border-slate-300">
                            <div class="p-1.5 px-3 border-r border-slate-300 font-semibold">TURNO: <span class="font-normal uppercase" x-text="header.shift"></span></div>
                            <div class="p-1.5 px-3 font-semibold">FECHA: <span class="font-normal" x-text="header.date"></span></div>
                        </div>
                        <div class="p-1.5 px-3 font-semibold bg-slate-50">
                            SUPERVISOR: <span class="font-normal uppercase" x-text="header.supervisor"></span>
                        </div>
                    </div>

                    <!-- Sección 1: Equipos y Maquinaria -->
                    <div class="mb-4">
                        <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[11px] uppercase tracking-wide mb-1">1. Equipos y Maquinaria en Turno</div>
                        <table class="w-full border-collapse border border-slate-400 text-[10px]">
                            <thead>
                                <tr class="bg-slate-100 text-slate-800 font-bold">
                                    <th class="border border-slate-400 p-1.5 text-left w-1/4">EQUIPOS</th>
                                    <th class="border border-slate-400 p-1.5 text-center w-28">COMBUSTIBLE</th>
                                    <th class="border border-slate-400 p-1.5 text-center w-28">HORÓMETROS / KM</th>
                                    <th class="border border-slate-400 p-1.5 text-center w-20">PRÓX. MANT.</th>
                                    <th class="border border-slate-400 p-1.5 text-left">OBSERVACIONES</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="eq in equipmentList" :key="eq.name">
                                    <tr>
                                        <td class="border border-slate-300 p-1.5 font-semibold" x-text="eq.name"></td>
                                        <td class="border border-slate-300 p-1.5 text-center">
                                            <div class="flex justify-center space-x-1 text-[9px]">
                                                <span :class="eq.fuel === '1/4' ? 'font-bold bg-slate-300 px-1 rounded' : 'text-slate-400'">1/4</span>
                                                <span :class="eq.fuel === '1/2' ? 'font-bold bg-slate-300 px-1 rounded' : 'text-slate-400'">1/2</span>
                                                <span :class="eq.fuel === '3/4' ? 'font-bold bg-slate-300 px-1 rounded' : 'text-slate-400'">3/4</span>
                                                <span :class="eq.fuel === 'Full' ? 'font-bold bg-slate-300 px-1 rounded' : 'text-slate-400'">Full</span>
                                            </div>
                                        </td>
                                        <td class="border border-slate-300 p-1.5 text-center" x-text="eq.horometer"></td>
                                        <td class="border border-slate-300 p-1.5 text-center" x-text="eq.nextMaint"></td>
                                        <td class="border border-slate-300 p-1.5" x-text="eq.obs"></td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>

                    <!-- Nota importante -->
                    <div class="bg-amber-50 border border-amber-300 text-amber-900 font-bold px-3 py-1.5 text-[11px] mb-4 text-center">
                        NOTA: <span class="font-normal" x-text="header.note"></span>
                    </div>

                    <!-- Sección 2: Actividades Realizadas -->
                    <div class="mb-4">
                        <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[11px] uppercase tracking-wide mb-1">2. Actividades Realizadas</div>
                        <table class="w-full border-collapse border border-slate-400 text-[10px]">
                            <thead>
                                <tr class="bg-slate-100 text-slate-800 font-bold">
                                    <th class="border border-slate-400 p-1.5 text-center w-8">#</th>
                                    <th class="border border-slate-400 p-1.5 text-left w-36">LUGAR ESPECÍFICO</th>
                                    <th class="border border-slate-400 p-1.5 text-left">ACTIVIDAD REALIZADA</th>
                                    <th class="border border-slate-400 p-1.5 text-center w-20">% AVANCE</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="(act, index) in activityList" :key="index">
                                    <tr>
                                        <td class="border border-slate-300 p-1.5 text-center font-bold" x-text="index + 1"></td>
                                        <td class="border border-slate-300 p-1.5 font-semibold" x-text="act.location"></td>
                                        <td class="border border-slate-300 p-1.5" x-text="act.description"></td>
                                        <td class="border border-slate-300 p-1.5 text-center font-bold" x-text="act.progress + '%'"></td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>

                    <!-- Sección 3: Estado de Instalaciones -->
                    <div class="mb-4">
                        <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[11px] uppercase tracking-wide mb-1">3. Estado de Instalaciones de Faena / Sala de Cambio</div>
                        <table class="w-full border-collapse border border-slate-400 text-[10px]">
                            <thead>
                                <tr class="bg-slate-100 text-slate-800 font-bold">
                                    <th class="border border-slate-400 p-1.5 text-left w-1/3">ELEMENTOS</th>
                                    <th class="border border-slate-400 p-1.5 text-center w-28">ESTADO</th>
                                    <th class="border border-slate-400 p-1.5 text-left">OBSERVACIONES</th>
                                </tr>
                            </thead>
                            <tbody>
                                <template x-for="fac in facilityList" :key="fac.element">
                                    <tr>
                                        <td class="border border-slate-300 p-1.5 font-semibold" x-text="fac.element"></td>
                                        <td class="border border-slate-300 p-1.5 text-center font-bold" :class="fac.status === 'BUENO' ? 'text-emerald-700' : (fac.status === 'REGULAR' ? 'text-amber-700' : 'text-red-700')" x-text="fac.status"></td>
                                        <td class="border border-slate-300 p-1.5" x-text="fac.obs"></td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
                    </div>

                </div>

                <!-- Pie de página del documento 1 -->
                <div class="text-[9px] text-slate-500 border-t border-slate-300 pt-2 flex justify-between">
                    <span x-text="header.company + ' - Control Operacional de Turno'"></span>
                    <span>Documento Oficial Generado Digitalmente</span>
                </div>

            </div>
        </div>

        <!-- SECCIÓN DE ANEXO FOTOGRÁFICO EXCLUSIVO (Última Página del PDF) -->
        <div class="mt-8 flex justify-center">
            <div id="report-annex" class="bg-white w-[210mm] min-h-[297mm] p-[15mm] shadow-2xl border border-slate-200 text-slate-900 text-xs relative flex flex-col justify-between">
                
                <div>
                    <!-- Cabecera de Anexo -->
                    <div class="border-2 border-slate-800 mb-6 grid grid-cols-12 bg-slate-50">
                        <div class="col-span-9 p-3 border-r-2 border-slate-800">
                            <span class="font-extrabold text-sm tracking-widest text-slate-900 uppercase block" x-text="header.company"></span>
                            <span class="font-bold text-xs text-corporate uppercase">ANEXO FOTOGRÁFICO - REGISTRO ANTES Y DESPUÉS</span>
                        </div>
                        <div class="col-span-3 p-3 flex flex-col justify-center items-center text-[10px] font-bold">
                            <span>Página 2 de 2</span>
                            <span class="text-[9px] text-slate-500 font-normal" x-text="header.date"></span>
                        </div>
                    </div>

                    <!-- Grid de Fotos Anexo -->
                    <div class="space-y-6">
                        <template x-for="(pair, index) in photoPairs" :key="index">
                            <div class="border border-slate-300 rounded-lg p-3 bg-slate-50/50">
                                <div class="flex justify-between items-center border-b border-slate-200 pb-1.5 mb-2.5">
                                    <span class="font-bold text-petroleum">COMPARATIVA N° <span x-text="index + 1"></span> - <span x-text="pair.location"></span></span>
                                    <span class="text-slate-600 text-[11px]" x-text="pair.description"></span>
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <!-- ANTES -->
                                    <div class="bg-white p-2.5 rounded border border-slate-200 text-center">
                                        <div class="font-bold text-amber-700 text-[10px] mb-1.5 flex items-center justify-center space-x-1">
                                            <i class="fa-solid fa-clock-rotate-left"></i><span>ANTES DE LA TAREA</span>
                                        </div>
                                        <div class="h-44 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1.5">
                                            <template x-if="pair.beforeImg">
                                                <img :src="pair.beforeImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.beforeImg">
                                                <span class="text-slate-400 italic">Sin imagen adjunta</span>
                                            </template>
                                        </div>
                                        <p class="text-[10px] text-slate-600 italic" x-text="pair.beforeNote || 'Sin observación específica'"></p>
                                    </div>

                                    <!-- DESPUÉS -->
                                    <div class="bg-white p-2.5 rounded border border-slate-200 text-center">
                                        <div class="font-bold text-emerald-700 text-[10px] mb-1.5 flex items-center justify-center space-x-1">
                                            <i class="fa-solid fa-circle-check"></i><span>DESPUÉS DE LA TAREA</span>
                                        </div>
                                        <div class="h-44 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1.5">
                                            <template x-if="pair.afterImg">
                                                <img :src="pair.afterImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.afterImg">
                                                <span class="text-slate-400 italic">Sin imagen adjunta</span>
                                            </template>
                                        </div>
                                        <p class="text-[10px] text-slate-600 italic" x-text="pair.afterNote || 'Sin observación específica'"></p>
                                    </div>
                                </div>
                            </div>
                        </template>
                        <template x-if="photoPairs.length === 0">
                            <div class="text-center py-16 text-slate-400 italic border border-dashed border-slate-300 rounded-xl">
                                No se han adjuntado registros fotográficos para el anexo.
                            </div>
                        </template>
                    </div>
                </div>

                <!-- Pie de página del anexo -->
                <div class="text-[9px] text-slate-500 border-t border-slate-300 pt-2 flex justify-between mt-6">
                    <span x-text="header.company + ' - Anexo Fotográfico de Faena'"></span>
                    <span>Fin del Informe Técnico</span>
                </div>

            </div>
        </div>

    </main>

    <!-- Script de lógica de la aplicación -->
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
                    date: '2026-03-12',
                    supervisor: 'HERNAN GONZALO TRONCOSO OÑATE',
                    note: 'REVISAR AIRE ACONDICIONADO DE SALA CAMBIO, OFICINA Y SALA REUNIONES'
                },

                equipmentList: [
                    { name: 'Camión aspirador 12', fuel: '3/4', horometer: '5853 / 5861', nextMaint: '4270', obs: 'Equipo operativo, recarga combustible.' },
                    { name: 'Camión aspirador 34', fuel: 'Full', horometer: '12693 / 12670', nextMaint: '12740', obs: 'Equipo Operativo, se recarga combustible 140 LTS.' },
                    { name: 'Mini cargador 450', fuel: '1/2', horometer: '2212.6 / 2214.6', nextMaint: '2500.0', obs: 'Equipo operativo.' },
                    { name: 'Camioneta VPBW 16', fuel: 'Full', horometer: '9633.1 / 9', nextMaint: '10.000', obs: 'Equipo operativo.' }
                ],

                activityList: [
                    { location: 'CT 135 C', description: 'LIMPIEZA MANUAL SECTOR PASILLO IZQUIERDO', progress: 100 },
                    { location: 'CH 2°, 3°', description: 'HUMECTACION DE CAMINOS 2 VECES (APOYO PRIMARIO)', progress: 100 },
                    { location: 'CT 135 C', description: 'LIMPIEZA MANUAL SECTOR PASILLO DERECHO', progress: 100 },
                    { location: 'SILICA', description: 'LIMPIEZA MANUAL SECTOR PARRILLA Y ACCESO', progress: 100 },
                    { location: 'FINO 2', description: 'ASPIRACION DE MATERIAL SECTRO PALTAFORMA, CORONA Y PASILLOS', progress: 100 },
                    { location: 'FINO 2', description: 'ASPIRACION DE MATERIAL SECTOR BASE, CONTORNO, MOTRIZY COPA DE AGUA', progress: 100 }
                ],

                facilityList: [
                    { element: 'CASILLEROS', status: 'BUENO', obs: 'OPERATIVO' },
                    { element: 'DUCHAS', status: 'BUENO', obs: 'OPERATIVO' },
                    { element: 'BAÑOS (WC)', status: 'BUENO', obs: 'Mantener puerta cerrada entrada' },
                    { element: 'URINARIOS', status: 'BUENO', obs: 'OK' },
                    { element: 'PORTA NOVA', status: 'BUENO', obs: 'OK' },
                    { element: 'JABONERAS', status: 'BUENO', obs: 'OK' },
                    { element: 'LAVA MANOS', status: 'BUENO', obs: 'REPONER 1 FOCO QUEMADO EN BAÑO' },
                    { element: 'ILUMINACION', status: 'BUENO', obs: 'OPERATIVO' }
                ],

                photoPairs: [
                    {
                        location: 'CT 135 C',
                        description: 'Limpieza de pasillo principal y retiro de material acumulado.',
                        beforeImg: '',
                        beforeNote: 'Acumulación de mineral en sector pasillo.',
                        afterImg: '',
                        afterNote: 'Sector despejado y limpio conforme a norma.'
                    }
                ],

                showNotification(msg) {
                    this.notificationText = msg;
                    this.notification = true;
                    setTimeout(() => { this.notification = false; }, 3000);
                },

                addEquipment() {
                    this.equipmentList.push({ name: '', fuel: 'Full', horometer: '', nextMaint: '', obs: '' });
                    this.showNotification('Equipo agregado correctamente');
                },
                removeEquipment(index) {
                    this.equipmentList.splice(index, 1);
                },

                addActivity() {
                    this.activityList.push({ location: '', description: '', progress: 100 });
                    this.showNotification('Actividad agregada');
                },
                removeActivity(index) {
                    this.activityList.splice(index, 1);
                },

                addFacility() {
                    this.facilityList.push({ element: '', status: 'BUENO', obs: '' });
                    this.showNotification('Elemento agregado');
                },
                removeFacility(index) {
                    this.facilityList.splice(index, 1);
                },

                addPhotoPair() {
                    this.photoPairs.push({ location: '', description: '', beforeImg: '', beforeNote: '', afterImg: '', afterNote: '' });
                    this.showNotification('Nueva comparativa fotográfica agregada');
                },
                removePhotoPair(index) {
                    this.photoPairs.splice(index, 1);
                },

                handleImageUpload(event, index, field) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            this.photoPairs[index][field] = e.target.result;
                            this.showNotification('Imagen cargada exitosamente');
                        };
                        reader.readAsDataURL(file);
                    }
                },

                exportPDF() {
                    this.showNotification('Generando PDF multipágina, por favor espere...');
                    
                    // Contenedor temporal combinando reporte principal + anexo fotográfico
                    const elementMain = document.getElementById('report-document');
                    const elementAnnex = document.getElementById('report-annex');

                    // Creamos un wrapper temporal para exportar todo de corrido en orden de páginas
                    const wrapper = document.createElement('div');
                    wrapper.style.width = '210mm';
                    wrapper.style.backgroundColor = '#ffffff';
                    
                    // Clonar nodos para PDF
                    const cloneMain = elementMain.cloneNode(true);
                    const cloneAnnex = elementAnnex.cloneNode(true);
                    
                    // Asegurar márgenes y saltos de página limpios
                    cloneMain.style.marginBottom = '20px';
                    
                    wrapper.appendChild(cloneMain);
                    if(this.photoPairs.length > 0) {
                        wrapper.appendChild(cloneAnnex);
                    }

                    const opt = {
                        margin:       10,
                        filename:     `Informe_Turno_Faena_${this.header.date}.pdf`,
                        image:        { type: 'jpeg', quality: 0.98 },
                        html2canvas:  { scale: 2, useCORS: true, letterRendering: true },
                        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
                    };

                    html2pdf().from(wrapper).set(opt).save().then(() => {
                        this.showNotification('PDF exportado exitosamente');
                    });
                }
            }
        }
    </script>
</body>
</html>