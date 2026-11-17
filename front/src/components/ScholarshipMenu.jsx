

export default function ScholarshipMenu({
  scholarships,
  onSelect
}) {
  return (
    <section className="border border-cyan-400 bg-[#020B34]/90 p-10">
      <h2 className="mb-12 text-center text-4xl font-black tracking-widest text-white">
        BECAS A SOLICITAR
      </h2>

      <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
        {scholarships.map((beca) => (
          <button
            key={beca.id}
            onClick={() => onSelect(beca)}
            className="border border-cyan-400 bg-slate-900/40 p-10 transition duration-300 hover:scale-105 hover:bg-cyan-900/20"
          >
            <div className="flex flex-col items-center gap-4">
              <div className="flex h-24 w-24 items-center justify-center rounded border border-cyan-400 text-5xl text-cyan-400">
                📄
              </div>

              <h3 className="text-center text-xl font-bold tracking-widest text-white">
                {beca.nombre}
              </h3>
            </div>
          </button>
        ))}
      </div>
    </section>
  )
}

