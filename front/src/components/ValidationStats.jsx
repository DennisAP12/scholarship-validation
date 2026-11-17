
export default function ValidationStats({
  validatedDocuments,
  totalDocuments
}) {
  const percentage = totalDocuments
    ? Math.round(
        (validatedDocuments / totalDocuments) * 100
      )
    : 0

  return (
    <div className="flex h-full flex-col items-center justify-center border border-cyan-400 p-8">
      <h3 className="mb-10 text-center text-sm font-bold uppercase tracking-[0.3em] text-white">
        Estadísticas de Validación
      </h3>

      <div className="relative flex h-56 w-56 items-center justify-center rounded-full bg-slate-100">
        <div
          className="absolute inset-0 rounded-full"
          style={{
            background: `conic-gradient(
              #22d3ee ${percentage}%,
              #1e293b ${percentage}%
            )`
          }}
        />

        <div className="z-10 flex h-44 w-44 items-center justify-center rounded-full bg-slate-100">
          <span className="text-3xl font-black text-slate-800">
            {percentage}%
          </span>
        </div>
      </div>

      <p className="mt-8 text-center text-sm text-cyan-300">
        {validatedDocuments} de {totalDocuments} documentos validados
      </p>
    </div>
  )
}

