import { useState } from 'react'

export default function DocumentCard({ title, onValidate }) {
  const [fileName, setFileName] = useState('')
  const [status, setStatus] = useState('idle')
  const [validated, setValidated] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  // Función para mapear el título de la tarjeta con el tipo que espera la API
  const getDocumentType = (title) => {
    const t = title.toLowerCase()
    if (t.includes('curp')) return 'curp'
    if (t.includes('acta')) return 'acta'
    if (t.includes('ine') || t.includes('identificación')) return 'identificacion'
    if (t.includes('domicilio')) return 'comprobante_domicilio'
    if (t.includes('inscripción') || t.includes('estudios') || t.includes('constancia')) return 'constancia_estudios'
    if (t.includes('solicitud')) return 'solicitud_beca'
    return 'identificacion' // Valor por defecto si no mapea ninguno
  }

  async function handleFileChange(event) {
    const file = event.target.files[0]
    if (!file) return

    setFileName(file.name)
    setStatus('processing')
    setErrorMessage('')

    // Preparar el archivo para enviar a Python
    const formData = new FormData()
    formData.append('tipo_documento', getDocumentType(title))
    formData.append('file', file)

    try {
      // Hacer la petición a nuestra API en Python
      const response = await fetch('http://localhost:8000/analizar', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()

      if (data.success && data.es_valido) {
        setStatus('success')
        // Contabilizar progreso general
        if (!validated) {
          onValidate()
          setValidated(true)
        }
      } else {
        setStatus('error')
        // Limpiar un poco el mensaje para que quepa en la tarjetita
        let msg = data.mensaje || data.error || 'Documento no válido'
        msg = msg.replace('⚠️ ADVERTENCIA: ', '').replace('⚠️ Atención: ', '')
        setErrorMessage(msg)
      }
    } catch (error) {
      console.error(error)
      setStatus('error')
      setErrorMessage('Error de conexión con la API')
    }
  }

  return (
    <label className={`group relative flex h-56 w-44 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border bg-white/5 p-4 text-center backdrop-blur-sm transition duration-300 hover:-translate-y-2 hover:shadow-2xl ${status === 'error' ? 'border-red-500/50 hover:border-red-400 hover:shadow-red-500/20' : status === 'success' ? 'border-green-500/50' : 'border-cyan-400/40 hover:border-cyan-300 hover:shadow-cyan-500/20 hover:bg-cyan-400/10'}`}>
      <input
        type="file"
        accept=".pdf,image/*"
        className="hidden"
        onChange={handleFileChange}
      />

      <div className={`absolute inset-0 transition duration-300 ${status === 'error' ? 'bg-red-500/0 group-hover:bg-red-500/5' : 'bg-cyan-400/0 group-hover:bg-cyan-400/5'}`} />

      <div className="mb-4 text-6xl transition duration-300 group-hover:scale-110">
        📄
      </div>

      <p className="mb-3 text-sm font-bold uppercase tracking-widest text-white">
        {title}
      </p>

      {!fileName && (
        <span className="text-xs text-cyan-300">
          Seleccionar archivo
        </span>
      )}

      {fileName && (
        <div className="mt-2 w-full text-center">
          <p className="mx-auto max-w-[120px] truncate text-xs text-white">
            {fileName}
          </p>

          {status === 'processing' && (
            <p className="mt-2 text-xs font-semibold text-yellow-400 animate-pulse">
              Analizando...
            </p>
          )}

          {status === 'success' && (
            <p className="mt-2 text-xs font-bold text-green-400">
              ¡Documento válido! ✔
            </p>
          )}

          {status === 'error' && (
            <div className="mt-2 text-xs text-red-400" title={errorMessage}>
              <span className="font-bold">❌ Rechazado:</span>
              <p className="line-clamp-2 text-[10px] mt-1 leading-tight">{errorMessage}</p>
            </div>
          )}
        </div>
      )}
    </label>
  )
}
