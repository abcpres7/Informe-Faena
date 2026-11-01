<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de Informe Operacional de Turno</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alpine.js CDN -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <!-- html2pdf.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        petroleum: '#005b60',
                        codelco: '#00857c',
                        darkslate: '#1e293b'
                    }
                }
            }
        }
    </script>
    <style>
        @media print {
            body { background: white !important; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
            .no-print { display: none !important; }
            .page-break { page-break-before: always; }
            .avoid-break { page-break-inside: avoid; }
        }
    </style>
</head>
<body class="bg-slate-100 min-h-screen text-slate-800 font-sans" x-data="reportApp()">

    <!-- BARRA DE ACCESO RÁPIDO Y CONTROLES (NO SALE EN PDF) -->
    <header class="no-print bg-slate-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="bg-teal-600 p-2 rounded-lg font-bold text-xl">CODELCO</div>
                <div>
                    <h1 class="font-bold text-lg leading-tight">Generador de Informes de Turno</h1>
                    <p class="text-xs text-slate-400">Sistema Oficial de Control Operacional</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <button @click="generatePDF()" class="bg-teal-600 hover:bg-teal-700 text-white font-semibold px-4 py-2 rounded-lg shadow transition flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    Generar y Descargar PDF
                </button>
            </div>
        </div>
    </header>

    <!-- FORMULARIO DE EDICIÓN RÁPIDA (NO SALE EN PDF) -->
    <section class="no-print max-w-7xl mx-auto px-4 py-6">
        <div class="bg-white rounded-xl shadow-md p-6 mb-6 border-t-4 border-teal-600">
            <h2 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                Panel de Edición de Datos del Turno
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Empresa Principal</label>
                    <input type="text" x-model="meta.empresa" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">División / Proyecto</label>
                    <input type="text" x-model="meta.division" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Área de Trabajo</label>
                    <input type="text" x-model="meta.area" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Turno</label>
                    <input type="text" x-model="meta.turno" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Fecha</label>
                    <input type="date" x-model="meta.fecha" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Supervisor Responsable</label>
                    <input type="text" x-model="meta.supervisor" class="w-full border rounded p-2 text-sm bg-slate-50">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Dotación / Personal Asignado</label>
                    <input type="text" x-model="meta.dotacion" class="w-full border rounded p-2 text-sm bg-slate-50" placeholder="Ej: 8 Operarios, 1 Supervisor">
                </div>
            </div>
        </div>
    </section>

    <!-- CONTENEDOR EXCLUSIVO PARA EL INFORME PDF -->
    <main class="max-w-[210mm] mx-auto bg-white shadow-2xl p-8 my-6 rounded-lg" id="pdf-content">

        <!-- ENCABEZADO OFICIAL -->
        <div class="border-b-2 border-teal-700 pb-4 mb-4">
            <div class="flex justify-between items-start">
                <div>
                    <div class="text-xs font-bold text-slate-500 uppercase tracking-wider" x-text="meta.empresa"></div>
                    <h2 class="text-xl font-extrabold text-petroleum tracking-wide mt-1">INFORME ENTREGA DE TURNO DIARIO</h2>
                    <p class="text-xs text-slate-600 font-semibold mt-0.5" x-text="'SISTEMA DE GESTIÓN INTEGRADA - ' + meta.division"></p>
                </div>
                <div class="text-right">
                    <span class="text-xs font-bold bg-teal-50 text-teal-800 px-3 py-1 rounded border border-teal-200">Página 1 de 2</span>
                    <div class="text-[10px] text-slate-400 mt-1">Código: SGI-FR-041</div>
                </div>
            </div>

            <!-- DATOS GENERALES -->
            <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-2 bg-slate-50 p-3 rounded border border-slate-200 text-xs">
                <div><span class="font-bold text-slate-600">ÁREA:</span> <span x-text="meta.area" class="text-slate-800 font-medium"></span></div>
                <div><span class="font-bold text-slate-600">TURNO:</span> <span x-text="meta.turno" class="text-slate-800 font-medium"></span></div>
                <div><span class="font-bold text-slate-600">FECHA:</span> <span x-text="meta.fecha" class="text-slate-800 font-medium"></span></div>
                <div><span class="font-bold text-slate-600">DOTACIÓN:</span> <span x-text="meta.dotacion" class="text-slate-800 font-medium"></span></div>
                <div class="col-span-2 md:col-span-4 mt-1 pt-1 border-t border-slate-200">
                    <span class="font-bold text-slate-600">SUPERVISOR:</span> <span x-text="meta.supervisor" class="text-slate-800 uppercase font-medium"></span>
                </div>
            </div>
        </div>

        <!-- SECCIÓN 1: EQUIPOS Y MAQUINARIA -->
        <div class="mb-6 avoid-break">
            <h3 class="bg-teal-700 text-white text-xs font-bold px-3 py-1.5 uppercase tracking-wider mb-2 flex justify-between items-center">
                <span>1. Equipos y Maquinaria en Turno</span>
                <button @click="addEquipo()" class="no-print bg-teal-800 hover:bg-teal-900 text-white text-[10px] px-2 py-0.5 rounded">+ Agregar Equipo</button>
            </h3>
            <table class="w-full text-left border-collapse text-[11px]">
                <thead>
                    <tr class="bg-slate-200 text-slate-700 border-b border-slate-300">
                        <th class="p-1.5 border">Equipos</th>
                        <th class="p-1.5 border text-center">Combustible</th>
                        <th class="p-1.5 border">Horómetros / KM</th>
                        <th class="p-1.5 border text-center">Próx. Mant.</th>
                        <th class="p-1.5 border">Observaciones</th>
                        <th class="no-print p-1.5 border text-center">Acción</th>
                    </tr>
                </thead>
                <tbody>
                    <template x-for="(eq, index) in equipos" :key="index">
                        <tr class="border-b border-slate-200">
                            <td class="p-1.5 border"><input type="text" x-model="eq.nombre" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                            <td class="p-1.5 border text-center">
                                <select x-model="eq.combustible" class="text-[10px] bg-transparent border rounded p-0.5">
                                    <option>1/4</option><option>1/2</option><option>3/4</option><option selected>Full</option>
                                </select>
                            </td>
                            <td class="p-1.5 border"><input type="text" x-model="eq.horometro" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                            <td class="p-1.5 border text-center"><input type="text" x-model="eq.mantencion" class="w-full bg-transparent text-center focus:bg-white focus:outline-none"></td>
                            <td class="p-1.5 border"><input type="text" x-model="eq.obs" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                            <td class="no-print p-1.5 border text-center">
                                <button @click="equipos.splice(index, 1)" class="text-red-500 font-bold hover:text-red-700">×</button>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>

        <!-- SECCIÓN 2: ACTIVIDADES REALIZADAS -->
        <div class="mb-6 avoid-break">
            <h3 class="bg-teal-700 text-white text-xs font-bold px-3 py-1.5 uppercase tracking-wider mb-2 flex justify-between items-center">
                <span>2. Actividades Realizadas en el Turno</span>
                <button @click="addActividad()" class="no-print bg-teal-800 hover:bg-teal-900 text-white text-[10px] px-2 py-0.5 rounded">+ Agregar Actividad</button>
            </h3>
            <table class="w-full text-left border-collapse text-[11px]">
                <thead>
                    <tr class="bg-slate-200 text-slate-700 border-b border-slate-300">
                        <th class="p-1.5 border w-10 text-center">#</th>
                        <th class="p-1.5 border w-32">Lugar Específico</th>
                        <th class="p-1.5 border">Actividad Realizada</th>
                        <th class="p-1.5 border w-20 text-center">% Avance</th>
                        <th class="no-print p-1.5 border w-12 text-center">Acción</th>
                    </tr>
                </thead>
                <tbody>
                    <template x-for="(act, index) in actividades" :key="index">
                        <tr class="border-b border-slate-200">
                            <td class="p-1.5 border text-center font-bold" x-text="index + 1"></td>
                            <td class="p-1.5 border"><input type="text" x-model="act.lugar" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                            <td class="p-1.5 border"><input type="text" x-model="act.descripcion" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                            <td class="p-1.5 border text-center"><input type="text" x-model="act.avance" class="w-full bg-transparent text-center focus:bg-white focus:outline-none"></td>
                            <td class="no-print p-1.5 border text-center">
                                <button @click="actividades.splice(index, 1)" class="text-red-500 font-bold hover:text-red-700">×</button>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>

        <!-- SECCIÓN 3: ESTADO DE INSTALACIONES -->
        <div class="mb-4 avoid-break">
            <h3 class="bg-teal-700 text-white text-xs font-bold px-3 py-1.5 uppercase tracking-wider mb-2">
                3. Estado de Instalaciones de Faena / Sala de Cambio
            </h3>
            <table class="w-full text-left border-collapse text-[11px]">
                <thead>
                    <tr class="bg-slate-200 text-slate-700 border-b border-slate-300">
                        <th class="p-1.5 border">Elementos</th>
                        <th class="p-1.5 border w-28 text-center">Estado</th>
                        <th class="p-1.5 border">Observaciones</th>
                    </tr>
                </thead>
                <tbody>
                    <template x-for="(inst, index) in instalaciones" :key="index">
                        <tr class="border-b border-slate-200">
                            <td class="p-1.5 border font-semibold text-slate-700" x-text="inst.elemento"></td>
                            <td class="p-1.5 border text-center">
                                <select x-model="inst.estado" class="text-[10px] bg-transparent border rounded p-0.5 font-bold text-teal-700">
                                    <option>BUENO</option>
                                    <option>REGULAR</option>
                                    <option>MALO</option>
                                    <option>NO OPERATIVO</option>
                                </select>
                            </td>
                            <td class="p-1.5 border"><input type="text" x-model="inst.obs" class="w-full bg-transparent focus:bg-white focus:outline-none"></td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>

        <!-- SALTO DE PÁGINA OBLIGATORIO PARA EL ANEXO FOTOGRÁFICO -->
        <div class="page-break pt-6"></div>

        <!-- ENCABEZADO DE LA SEGUNDA PÁGINA (ANEXO) -->
        <div class="border-b-2 border-teal-700 pb-3 mb-4">
            <div class="flex justify-between items-start">
                <div>
                    <div class="text-xs font-bold text-slate-500 uppercase tracking-wider" x-text="meta.empresa"></div>
                    <h2 class="text-lg font-extrabold text-petroleum tracking-wide mt-0.5">ANEXO FOTOGRÁFICO - REGISTRO ANTES Y DESPUÉS</h2>
                </div>
                <div class="text-right">
                    <span class="text-xs font-bold bg-teal-50 text-teal-800 px-3 py-1 rounded border border-teal-200">Página 2 de 2</span>
                    <div class="text-[10px] text-slate-400 mt-1" x-text="meta.fecha"></div>
                </div>
            </div>
        </div>

        <!-- SECCIÓN DE FOTOS COMPARATIVAS -->
        <div class="mb-4">
            <div class="flex justify-between items-center mb-3">
                <p class="text-xs text-slate-600 font-medium">Registro visual comparativo de las tareas ejecutadas en terreno durante el turno:</p>
                <button @click="addComparativa()" class="no-print bg-teal-700 hover:bg-teal-800 text-white text-xs px-3 py-1 rounded font-bold shadow">+ Agregar Comparativa</button>
            </div>

            <template x-for="(comp, index) in comparativas" :key="index">
                <div class="mb-6 p-3 border border-slate-300 rounded-lg bg-slate-50 avoid-break">
                    <div class="flex justify-between items-center mb-2 border-b pb-1">
                        <span class="text-xs font-bold text-petroleum uppercase" x-text="'Comparativa N&deg; ' + (index + 1) + ' - ' + (comp.titulo || 'Sin Título')"></span>
                        <button @click="comparativas.splice(index, 1)" class="no-print text-red-500 font-bold text-xs hover:text-red-700">Eliminar</button>
                    </div>

                    <!-- Input para título y descripción en pantalla -->
                    <div class="no-print grid grid-cols-2 gap-2 mb-3">
                        <input type="text" x-model="comp.titulo" placeholder="Título / Lugar (Ej: Limpieza de Pasillo CT-135)" class="text-xs border p-1.5 rounded">
                        <input type="text" x-model="comp.descripcion" placeholder="Descripción breve de la tarea" class="text-xs border p-1.5 rounded">
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <!-- ANTES -->
                        <div class="bg-white p-2 border rounded text-center">
                            <span class="block text-[10px] font-bold text-red-600 uppercase mb-1 bg-red-50 py-0.5 rounded">Antes de la Tarea</span>
                            <div class="h-40 border-2 border-dashed border-slate-300 rounded flex items-center justify-center overflow-hidden relative bg-slate-100">
                                <template x-if="comp.imgAntes">
                                    <img :src="comp.imgAntes" class="w-full h-full object-cover">
                                </template>
                                <template x-if="!comp.imgAntes">
                                    <span class="text-[10px] text-slate-400">Sin imagen adjunta</span>
                                </template>
                            </div>
                            <input type="file" @change="loadFile($event, index, 'antes')" accept="image/*" class="no-print mt-2 text-[10px] w-full file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-[10px] file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100">
                        </div>

                        <!-- DESPUÉS -->
                        <div class="bg-white p-2 border rounded text-center">
                            <span class="block text-[10px] font-bold text-emerald-600 uppercase mb-1 bg-emerald-50 py-0.5 rounded">Después de la Tarea</span>
                            <div class="h-40 border-2 border-dashed border-slate-300 rounded flex items-center justify-center overflow-hidden relative bg-slate-100">
                                <template x-if="comp.imgDespues">
                                    <img :src="comp.imgDespues" class="w-full h-full object-cover">
                                </template>
                                <template x-if="!comp.imgDespues">
                                    <span class="text-[10px] text-slate-400">Sin imagen adjunta</span>
                                </template>
                            </div>
                            <input type="file" @change="loadFile($event, index, 'despues')" accept="image/*" class="no-print mt-2 text-[10px] w-full file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:text-[10px] file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100">
                        </div>
                    </div>
                </div>
            </template>
        </div>

        <!-- FIRMA Y PIE DE PÁGINA -->
        <div class="mt-8 pt-4 border-t border-slate-300 text-center text-[10px] text-slate-500 avoid-break">
            <div class="flex justify-around mb-6">
                <div class="text-center">
                    <div class="w-48 border-b border-slate-400 mx-auto mb-1"></div>
                    <span class="font-bold text-slate-700" x-text="meta.supervisor"></span><br>
                    <span>Firma Supervisor de Turno</span>
                </div>
                <div class="text-center">
                    <div class="w-48 border-b border-slate-400 mx-auto mb-1"></div>
                    <span class="font-bold text-slate-700">Control Operacional Faena</span><br>
                    <span>V°B° Administración</span>
                </div>
            </div>
            <p class="font-semibold text-slate-600" x-text="meta.empresa + ' - Control Operacional de Turno | Documento Oficial Generado Digitalmente'"></p>
        </div>

    </main>

    <!-- SCRIPT DE LÓGICA CON ALPINE.JS -->
    <script>
        function reportApp() {
            return {
                meta: {
                    empresa: 'CODELCO - DIVISIÓN TENIENTE',
                    division: 'DIVISIÓN TENIENTE',
                    area: 'ÁREA CHANCADO SECUNDARIO - TERCIARIO',
                    turno: 'TURNO B, NOCHE',
                    fecha: new Date().toISOString().split('T')[0],
                    supervisor: 'HERNAN GONZALO TRONCOSO OÑATE',
                    dotacion: '8 Operarios, 1 Supervisor'
                },
                equipos: [
                    { nombre: 'Camión aspirador 12', combustible: 'Full', horometro: '5853 / 5861', mantencion: '4270', obs: 'Equipo operativo' },
                    { nombre: 'Camión aspirador 34', combustible: 'Full', horometro: '12693 / 12670', mantencion: '12740', obs: 'Se recarga combustible' },
                    { nombre: 'Mini cargador 450', combustible: 'Full', horometro: '2212.6 / 2214.6', mantencion: '2500.0', obs: 'Equipo operativo' },
                    { nombre: 'Camioneta VPBW 16', combustible: 'Full', horometro: '9633.1 / 9', mantencion: '10000', obs: 'Equipo operativo' }
                ],
                actividades: [
                    { lugar: 'CT 135 C', descripcion: 'LIMPIEZA MANUAL SECTOR PASILLO IZQUIERDO', avance: '100%' },
                    { lugar: 'CH 2°, 3°', descripcion: 'HUMECTACION DE CAMINOS 2 VECES (APOYO PRIMARIO)', avance: '100%' },
                    { lugar: 'SILICA', descripcion: 'LIMPIEZA MANUAL SECTOR PARRILLA Y ACCESO', avance: '100%' },
                    { lugar: 'FINO 2', descripcion: 'ASPIRACION DE MATERIAL SECTOR PLATAFORMA Y CORONA', avance: '100%' }
                ],
                instalaciones: [
                    { elemento: 'CASILLEROS', estado: 'BUENO', obs: 'OPERATIVO' },
                    { elemento: 'DUCHAS', estado: 'BUENO', obs: 'OPERATIVO' },
                    { elemento: 'BAÑOS (WC)', estado: 'BUENO', obs: 'Mantener puerta cerrada' },
                    { elemento: 'URINARIOS', estado: 'BUENO', obs: 'OK' },
                    { elemento: 'PORTA NOVA', estado: 'BUENO', obs: 'OK' },
                    { elemento: 'JABONERAS', estado: 'BUENO', obs: 'OK' },
                    { elemento: 'LAVA MANOS', estado: 'BUENO', obs: 'REPONER 1 FOCO QUEMADO' },
                    { elemento: 'ILUMINACION', estado: 'BUENO', obs: 'OPERATIVO' }
                ],
                comparativas: [
                    { titulo: 'CT 135 C - Pasillo Principal', descripcion: 'Limpieza de pasillo y retiro de material acumulado', imgAntes: '', imgDespues: '' }
                ],
                addEquipo() {
                    this.equipos.push({ nombre: '', combustible: 'Full', horometro: '', mantencion: '', obs: '' });
                },
                addActividad() {
                    this.actividades.push({ lugar: '', descripcion: '', avance: '100%' });
                },
                addComparativa() {
                    this.comparativas.push({ titulo: '', descripcion: '', imgAntes: '', imgDespues: '' });
                },
                loadFile(event, index, tipo) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            if (tipo === 'antes') {
                                this.comparativas[index].imgAntes = e.target.result;
                            } else {
                                this.comparativas[index].imgDespues = e.target.result;
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                },
                generatePDF() {
                    const element = document.getElementById('pdf-content');
                    const opt = {
                        margin:       5,
                        filename:     `Informe_Turno_${this.meta.fecha}.pdf`,
                        image:        { type: 'jpeg', quality: 0.98 },
                        html2canvas:  { scale: 2, useCORS: true, letterRendering: true },
                        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
                    };
                    html2pdf().from(element).set(opt).save();
                }
            }
        }
    </script>
</body>
</html>
