
import { useState } from 'react'

import DocumentCard from './DocumentCard'
import ValidationStats from './ValidationStats'

export default function ScholarshipDetails({
  scholarship,
  onBack
}) {
  const totalDocuments =
    scholarship.studentDocuments.length +
    scholarship.tutorDocuments.length

  const [validatedDocuments, setValidatedDocuments] =
    useState(0)

  function handleValidate() {
    setValidatedDocuments((prev) => {
      if (prev >= totalDocuments) return prev

      return prev + 1
    })
  }

  return (

   <section className="rounded-3xl border border-cyan-400/30 bg-white/5 p-8 shadow-2xl shadow-cyan-500/10 backdrop-blur-md">


      <button
        onClick={onBack}
        className="mb-8 rounded-xl border border-cyan-400 px-5 py-2 text-white transition duration-300 hover:bg-cyan-400 hover:text-slate-900"
      >
        ← Regresar
      </button>

   <h2 className="mb-12 bg-gradient-to-r from-cyan-300 to-blue-500 bg-clip-text text-5xl font-black uppercase tracking-[0.3em] text-transparent">


        DOCUMENTOS BECA {scholarship.nombre}
      </h2>

      <div className="grid gap-10 lg:grid-cols-[1fr_350px]">
        <div>
          <div className="mb-12">
            <h3 className="mb-8 text-2xl font-black uppercase tracking-widest text-white">
              DOCUMENTOS DEL ESTUDIANTE
            </h3>

            <div className="grid grid-cols-2 gap-6 md:grid-cols-3">
              {scholarship.studentDocuments.map((doc) => (
                <DocumentCard
                  key={doc}
                  title={doc}
                  onValidate={handleValidate}
                />
              ))}
            </div>
          </div>

          {scholarship.tutorDocuments && scholarship.tutorDocuments.length > 0 && (
            <div>
              <h3 className="mb-8 text-2xl font-black uppercase tracking-widest text-white">
                DOCUMENTOS DEL PADRE, MADRE O TUTOR
              </h3>

              <div className="grid grid-cols-2 gap-6 md:grid-cols-3">
                {scholarship.tutorDocuments.map((doc) => (
                  <DocumentCard
                    key={doc}
                    title={doc}
                    onValidate={handleValidate}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        <ValidationStats
          validatedDocuments={validatedDocuments}
          totalDocuments={totalDocuments}
        />
      </div>
    </section>
  )
}

