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
        
        /* Estilos de Impresión y PDF Impecable */
        @media print {
            .no-print { display: none !important; }
            body { background: white !important; margin: 0; padding: 0; }
            .print-page {
                box-shadow: none !important;
                border: none !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 5mm !important;
            }
        }

        /* Estructura A4 optimizada para renderizado PDF */
        .pdf-page {
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

    <!-- Header Principal (No imprime) -->
    <header class="no-print bg-petroleum text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
            <div class="flex items-center space-x-3">
                <div class="bg-corporate p-2.5 rounded-lg text-white shadow">
                    <i class="fa-solid fa-industry text-xl"></i>
                </div>
                <div>
                    <h1 class="font-bold text-base sm:text-lg tracking-wide">MINING REPORT PRO</h1>
                    <p class="text-[11px] text-slate-400">Sistema de Información de Faena y Anexos Fotográficos</p>
                </div>
            </div>
            <div class="flex items-center space-x-2 w-full sm:w-auto justify-end">
                <button @click="activeTab = 'editor'" :class="activeTab === 'editor' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2 rounded-lg text-xs font-medium transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-pen-to-square"></i>
                    <span>Formulario</span>
                </button>
                <button @click="activeTab = 'preview'" :class="activeTab === 'preview' ? 'bg-corporate text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'" class="px-3 py-2 rounded-lg text-xs font-medium transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-eye"></i>
                    <span>Ver Previa</span>
                </button>
                <button @click="window.print()" class="bg-slate-700 hover:bg-slate-600 text-white px-3 py-2 rounded-lg text-xs font-semibold transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-print"></i>
                    <span class="hidden sm:inline">Imprimir</span>
                </button>
                <button @click="exportPDF()" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-xs font-semibold transition shadow flex items-center space-x-1.5">
                    <i class="fa-solid fa-file-pdf"></i>
                    <span>Descargar PDF</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Notificación flotante de éxito -->
    <div x-show="notification" x-transition class="no-print fixed bottom-5 right-5 z-50 bg-slate-900 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center space-x-3 border-l-4 border-corporate">
        <i class="fa-solid fa-circle-check text-corporate text-lg"></i>
        <span class="text-xs sm:text-sm font-medium" x-text="notificationText"></span>
    </div>

    <main class="max-w-7xl mx-auto px-2 sm:px-4 py-6 w-full flex-grow">
        
        <!-- VISTA 1: EDITOR DE DATOS (FORMULARIO MOBILE FIRST) -->
        <div x-show="activeTab === 'editor'" class="no-print space-y-6">
            
            <!-- Modal / Card Guía de GitHub Pages -->
            <div x-data="{ showGithubHelp: false }" class="bg-slate-900 text-white rounded-xl p-4 shadow-lg border border-slate-700">
                <div class="flex justify-between items-center cursor-pointer" @click="showGithubHelp = !showGithubHelp">
                    <div class="flex items-center space-x-2">
                        <i class="fa-brands fa-github text-corporate text-lg"></i>
                        <span class="text-xs font-bold tracking-wide">¿CÓMO VER ESTA APP EN EL CELULAR CON GITHUB PAGES?</span>
                    </div>
                    <i class="fa-solid" :class="showGithubHelp ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                </div>
                <div x-show="showGithubHelp" x-transition class="mt-3 text-xs text-slate-300 space-y-2 border-t border-slate-800 pt-3">
                    <p>Para tener esta app como aplicación web accesible desde cualquier celular o PC:</p>
                    <ol class="list-decimal list-inside space-y-1 text-slate-300">
                        <li>Crea un repositorio público en <strong>GitHub.com</strong> (ej: <code class="bg-slate-800 text-corporate px-1 rounded">informe-faena</code>).</li>
                        <li>Sube este archivo guardándolo obligatoriamente con el nombre <strong><code class="bg-slate-800 text-corporate px-1 rounded">index.html</code></strong>.</li>
                        <li>En GitHub, ve a <strong>Settings &gt; Pages</strong>.</li>
                        <li>En <em>Branch</em> selecciona <strong>main</strong> (o <em>master</em>) y guarda.</li>
                        <li>En 1 minuto tendrás un enlace web que podrás abrir directamente en Chrome o Safari desde tu teléfono móvil.</li>
                    </ol>
                </div>
            </div>

            <!-- Tarjeta 1: Cabecera General y Dotación -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-building text-corporate"></i>
                        <span>1. Datos de Empresa, Faena y Dotación</span>
                    </h2>
                    <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-1 rounded font-medium">Formato Oficial</span>
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
                    <!-- CAMPO: DOTACIÓN TOTAL O PERSONAL ASIGNADO -->
                    <div class="sm:col-span-2 lg:col-span-3 bg-teal-50/60 border border-teal-200 p-3 rounded-lg">
                        <label class="block text-xs font-bold text-corporateDark mb-1 flex items-center space-x-1.5">
                            <i class="fa-solid fa-users text-corporate"></i>
                            <span>Dotación Total / Personal Asignado en Turno</span>
                        </label>
                        <input type="text" x-model="header.workforce" placeholder="Ej: 12 Personas (2 Operadores Camión, 1 Mini Cargador, 8 Aseo Industrial, 1 Apr)" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 bg-white focus:ring-2 focus:ring-corporate focus:outline-none">
                    </div>
                </div>
                <div class="mt-4">
                    <label class="block text-xs font-semibold text-slate-600 mb-1">Nota General u Observación Crítica</label>
                    <input type="text" x-model="header.note" class="w-full text-xs sm:text-sm border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-corporate focus:outline-none">
                </div>
            </div>

            <!-- Tarjeta 2: Equipos y Maquinaria -->
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-truck-monster text-corporate"></i>
                        <span>2. Registro de Equipos y Maquinaria</span>
                    </h2>
                    <button @click="addEquipment()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Añadir Equipo</span>
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
                                    <td class="p-1.5">
                                        <input type="text" x-model="eq.name" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5 text-center">
                                        <select x-model="eq.fuel" class="w-full border border-slate-200 rounded p-1.5 text-xs bg-white">
                                            <option value="1/4">1/4</option>
                                            <option value="1/2">1/2</option>
                                            <option value="3/4">3/4</option>
                                            <option value="Full">Full</option>
                                        </select>
                                    </td>
                                    <td class="p-1.5">
                                        <input type="text" x-model="eq.horometer" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5">
                                        <input type="text" x-model="eq.nextMaint" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5">
                                        <input type="text" x-model="eq.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5 text-center">
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
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-list-check text-corporate"></i>
                        <span>3. Actividades Realizadas</span>
                    </h2>
                    <button @click="addActivity()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Añadir Actividad</span>
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
                                    <td class="p-1.5">
                                        <input type="text" x-model="act.location" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5">
                                        <input type="text" x-model="act.description" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5 text-center">
                                        <input type="number" min="0" max="100" x-model="act.progress" class="w-16 border border-slate-200 rounded p-1.5 text-xs text-center">
                                    </td>
                                    <td class="p-1.5 text-center">
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
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                    <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                        <i class="fa-solid fa-house-chimney text-corporate"></i>
                        <span>4. Estado de Instalaciones de Faena / Sala de Cambio</span>
                    </h2>
                    <button @click="addFacility()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Añadir Elemento</span>
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
                                    <td class="p-1.5">
                                        <input type="text" x-model="fac.element" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5">
                                        <select x-model="fac.status" class="w-full border border-slate-200 rounded p-1.5 text-xs bg-white font-medium" :class="fac.status === 'BUENO' ? 'text-emerald-600' : (fac.status === 'REGULAR' ? 'text-amber-600' : 'text-red-600')">
                                            <option value="BUENO">BUENO / OPERATIVO</option>
                                            <option value="REGULAR">REGULAR</option>
                                            <option value="MALO">MALO / DEFECTUOSO</option>
                                        </select>
                                    </td>
                                    <td class="p-1.5">
                                        <input type="text" x-model="fac.obs" class="w-full border border-slate-200 rounded p-1.5 text-xs">
                                    </td>
                                    <td class="p-1.5 text-center">
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
            <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 sm:p-6">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-3 mb-4 border-b border-slate-100">
                    <div>
                        <h2 class="text-sm sm:text-base font-bold text-petroleum flex items-center space-x-2">
                            <i class="fa-solid fa-camera-retro text-corporate"></i>
                            <span>5. Anexo Fotográfico (Antes y Después)</span>
                        </h2>
                        <p class="text-[11px] text-slate-500 mt-0.5">Se colocará automáticamente en la última hoja del informe sin cortar las fotos.</p>
                    </div>
                    <button @click="addPhotoPair()" class="bg-corporate hover:bg-corporateDark text-white text-xs px-3 py-1.5 rounded-lg transition font-medium flex items-center space-x-1">
                        <i class="fa-solid fa-plus"></i><span>Nueva Comparativa</span>
                    </button>
                </div>
                
                <div class="space-y-6">
                    <template x-for="(pair, index) in photoPairs" :key="index">
                        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 sm:p-4 relative">
                            <div class="flex justify-between items-center mb-3">
                                <span class="text-xs font-bold text-petroleum uppercase bg-slate-200 px-2 py-0.5 rounded">Comparativa N&deg; <span x-text="index + 1"></span></span>
                                <button @click="removePhotoPair(index)" class="text-red-500 hover:text-red-700 text-xs font-medium flex items-center space-x-1">
                                    <i class="fa-solid fa-trash-can"></i><span>Eliminar</span>
                                </button>
                            </div>
                            
                            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-3">
                                <div>
                                    <label class="block text-[11px] font-semibold text-slate-600 mb-1">Ubicación / Sector</label>
                                    <input type="text" x-model="pair.location" placeholder="Ej: CT 135 C" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                                <div class="sm:col-span-2">
                                    <label class="block text-[11px] font-semibold text-slate-600 mb-1">Descripción de la tarea ejecutada</label>
                                    <input type="text" x-model="pair.description" placeholder="Ej: Limpieza manual de pasillo y descolgado" class="w-full text-xs border border-slate-300 rounded p-2 bg-white">
                                </div>
                            </div>

                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-200">
                                <!-- ANTES -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-amber-700 mb-1.5 flex items-center space-x-1">
                                        <i class="fa-solid fa-clock-rotate-left"></i><span>FOTO ANTES</span>
                                    </label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-20 h-20 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.beforeImg">
                                                <img :src="pair.beforeImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.beforeImg">
                                                <i class="fa-solid fa-image text-slate-300 text-xl"></i>
                                            </template>
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'beforeImg')" class="w-full text-[10px] text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-[10px] file:font-semibold file:bg-amber-50 file:text-amber-700 hover:file:bg-amber-100">
                                            <input type="text" x-model="pair.beforeNote" placeholder="Observación del estado previo" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>

                                <!-- DESPUÉS -->
                                <div class="bg-white p-3 rounded-lg border border-slate-200">
                                    <label class="block text-xs font-bold text-emerald-700 mb-1.5 flex items-center space-x-1">
                                        <i class="fa-solid fa-circle-check"></i><span>FOTO DESPUÉS</span>
                                    </label>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-20 h-20 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden shrink-0">
                                            <template x-if="pair.afterImg">
                                                <img :src="pair.afterImg" class="w-full h-full object-cover">
                                            </template>
                                            <template x-if="!pair.afterImg">
                                                <i class="fa-solid fa-image text-slate-300 text-xl"></i>
                                            </template>
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <input type="file" accept="image/*" @change="handleImageUpload($event, index, 'afterImg')" class="w-full text-[10px] text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-[10px] file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100">
                                            <input type="text" x-model="pair.afterNote" placeholder="Observación del trabajo finalizado" class="mt-2 w-full text-xs border border-slate-200 rounded p-1.5">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

        </div>

        <!-- VISTA 2 / CONTENEDOR DE INFORME IMPRESO Y PREVIEW (Formato Oficial A4 Corregido) -->
        <div class="flex justify-center w-full overflow-x-auto">
            <div id="full-report-container" class="my-2 shadow-2xl print-page">
                
                <!-- PÁGINA 1: INFORME DE TURNO -->
                <div class="pdf-page flex flex-col justify-between">
                    <div>
                        <!-- Cabecera del Informe -->
                        <div class="border-2 border-slate-800 mb-3 grid grid-cols-12 text-center">
                            <div class="col-span-4 border-r-2 border-slate-800 p-2 flex items-center justify-center bg-slate-50">
                                <div>
                                    <span class="font-extrabold text-xs tracking-wider text-slate-900 uppercase block" x-text="header.company"></span>
                                    <span class="text-[8px] text-slate-500 font-bold">SISTEMA INTEGRADO DE GESTIÓN</span>
                                </div>
                            </div>
                            <div class="col-span-6 border-r-2 border-slate-800 p-2 flex items-center justify-center bg-white">
                                <span class="font-bold text-xs tracking-wide uppercase" x-text="header.title"></span>
                            </div>
                            <div class="col-span-2 p-2 flex flex-col justify-center items-center text-[9px] font-bold bg-slate-50">
                                <span>PÁG. 1 DE 2</span>
                            </div>
                        </div>

                        <!-- Datos Generales e Identificación -->
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

                        <!-- Sección 1: Equipos y Maquinaria -->
                        <div class="mb-3 avoid-break">
                            <div class="bg-slate-800 text-white font-bold px-3 py-1 text-[10px] uppercase tracking-wide mb-1">1. Equipos y Maquinaria en Turno</div>
                            <table class="w-full border-collapse border border-slate-400 text-[9px]">
                                <thead>
                                    <tr class="bg-slate-100 text-slate-800 font-bold">
                                        <th class="border border-slate-400 p-1 text-left w-1/4">EQUIPOS</th>
                                        <th class="border border-slate-400 p-1 text-center w-20">COMBUSTIBLE</th>
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

                        <!-- Nota importante -->
                        <div class="bg-amber-50 border border-amber-300 text-amber-900 font-bold px-3 py-1 text-[9px] mb-3 avoid-break">
                            NOTA: <span class="font-normal" x-text="header.note"></span>
                        </div>

                        <!-- Sección 2: Actividades Realizadas -->
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

                        <!-- Sección 3: Estado de Instalaciones -->
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
                                            <td class="border border-slate-300 p-1 text-center font-bold" :class="fac.status === 'BUENO' ? 'text-emerald-700' : (fac.status === 'REGULAR' ? 'text-amber-700' : 'text-red-700')" x-text="fac.status"></td>
                                            <td class="border border-slate-300 p-1" x-text="fac.obs"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>

                    </div>

                    <!-- Pie de página 1 -->
                    <div class="text-[8px] text-slate-500 border-t border-slate-300 pt-1 flex justify-between mt-2">
                        <span x-text="header.company + ' - Control Operacional de Turno'"></span>
                        <span>Documento Digital Generado Oficial</span>
                    </div>
                </div>

                <!-- SALTO DE PÁGINA FORZADO PARA EL ANEXO FOTOGRÁFICO -->
                <div class="force-page-break"></div>

                <!-- PÁGINA 2: ANEXO FOTOGRÁFICO (SIEMPRE EN LA ÚLTIMA HOJA) -->
                <div class="pdf-page flex flex-col justify-between">
                    <div>
                        <!-- Cabecera de Anexo -->
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

                        <!-- Grid de Fotos Anexo -->
                        <div class="space-y-4">
                            <template x-for="(pair, index) in photoPairs" :key="index">
                                <div class="border border-slate-400 rounded-lg p-2.5 bg-slate-50/50 avoid-break">
                                    <div class="flex justify-between items-center border-b border-slate-300 pb-1 mb-2">
                                        <span class="font-bold text-slate-800 text-[10px]">COMPARATIVA N&deg; <span x-text="index + 1"></span> - <span x-text="pair.location"></span></span>
                                        <span class="text-slate-600 text-[9px]" x-text="pair.description"></span>
                                    </div>
                                    <div class="grid grid-cols-2 gap-3">
                                        <!-- ANTES -->
                                        <div class="bg-white p-2 rounded border border-slate-300 text-center">
                                            <div class="font-bold text-amber-700 text-[9px] mb-1 flex items-center justify-center space-x-1">
                                                <i class="fa-solid fa-clock-rotate-left"></i><span>ANTES DE LA TAREA</span>
                                            </div>
                                            <div class="h-36 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1">
                                                <template x-if="pair.beforeImg">
                                                    <img :src="pair.beforeImg" class="w-full h-full object-cover">
                                                </template>
                                                <template x-if="!pair.beforeImg">
                                                    <span class="text-slate-400 italic text-[9px]">Sin foto adjunta</span>
                                                </template>
                                            </div>
                                            <p class="text-[9px] text-slate-600 italic truncate" x-text="pair.beforeNote || 'Estado previo'"></p>
                                        </div>

                                        <!-- DESPUÉS -->
                                        <div class="bg-white p-2 rounded border border-slate-300 text-center">
                                            <div class="font-bold text-emerald-700 text-[9px] mb-1 flex items-center justify-center space-x-1">
                                                <i class="fa-solid fa-circle-check"></i><span>DESPUÉS DE LA TAREA</span>
                                            </div>
                                            <div class="h-36 bg-slate-100 rounded border border-slate-200 flex items-center justify-center overflow-hidden mb-1">
                                                <template x-if="pair.afterImg">
                                                    <img :src="pair.afterImg" class="w-full h-full object-cover">
                                                </template>
                                                <template x-if="!pair.afterImg">
                                                    <span class="text-slate-400 italic text-[9px]">Sin foto adjunta</span>
                                                </template>
                                            </div>
                                            <p class="text-[9px] text-slate-600 italic truncate" x-text="pair.afterNote || 'Resultado final'"></p>
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </div>
                    </div>

                    <!-- Pie de página 2 -->
                    <div class="text-[8px] text-slate-500 border-t border-slate-300 pt-1 flex justify-between mt-4">
                        <span x-text="header.company + ' - Registro Fotográfico de Evidencia'"></span>
                        <span>Fin del Informe Técnico</span>
                    </div>
                </div>

            </div>
        </div>

    </main>

    <!-- Footer explicativo (No imprime) -->
    <footer class="no-print bg-petroleum text-slate-400 text-xs py-4 border-t border-slate-800">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p>Mining & Faena Report Pro - Diseñado para Operaciones Mineras e Industriales</p>
        </div>
    </footer>

    <!-- Lógica de Aplicación -->
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
                    { name: 'Camión aspirador 34', fuel: 'Full', horometer: '12693 / 12670', nextMaint: '12740', obs: 'Equipo Operativo, se recarga combustible 140 LTS.' },
                    { name: 'Mini cargador 450', fuel: '1/2', horometer: '2212.6 / 2214.6', nextMaint: '2500.0', obs: 'Equipo operativo.' },
                    { name: 'Camioneta VPBW 16', fuel: 'Full', horometer: '9633.1 / 9', nextMaint: '10.000', obs: 'Equipo operativo.' }
                ],

                activityList: [
                    { location: 'CT 135 C', description: 'LIMPIEZA MANUAL SECTOR PASILLO IZQUIERDO', progress: 100 },
                    { location: 'CH 2°, 3°', description: 'HUMECTACION DE CAMINOS 2 VECES (APOYO PRIMARIO)', progress: 100 },
                    { location: 'CT 135 C', description: 'LIMPIEZA MANUAL SECTOR PASILLO DERECHO', progress: 100 },
                    { location: 'SILICA', description: 'LIMPIEZA MANUAL SECTOR PARRILLA Y ACCESO', progress: 100 },
                    { location: 'FINO 2', description: 'ASPIRACION DE MATERIAL SECTOR PLATAFORMA, CORONA Y PASILLOS', progress: 100 },
                    { location: 'FINO 2', description: 'ASPIRACION DE MATERIAL SECTOR BASE, CONTORNO Y COPA DE AGUA', progress: 100 }
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
                    this.showNotification('Equipo agregado');
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
                            this.showNotification('Fotografía cargada correctamente');
                        };
                        reader.readAsDataURL(file);
                    }
                },

                exportPDF() {
                    this.showNotification('Generando PDF completo...');
                    
                    const element = document.getElementById('full-report-container');

                    const opt = {
                        margin:       0,
                        filename:     `Informe_Turno_${this.header.date}.pdf`,
                        image:        { type: 'jpeg', quality: 0.98 },
                        html2canvas:  { 
                            scale: 2, 
                            useCORS: true, 
                            logging: false,
                            scrollY: 0,
                            windowWidth: 800
                        },
                        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
                        pagebreak:    { mode: ['css', 'legacy'] }
                    };

                    html2pdf().set(opt).from(element).save().then(() => {
                        this.showNotification('¡PDF descargado con éxito en 2 páginas exactas!');
                    }).catch(err => {
                        console.error('Error generando PDF:', err);
                        this.showNotification('Error al exportar. Pruebe el botón Imprimir.');
                    });
                }
            }
        }
    </script>
</body>
</html>
