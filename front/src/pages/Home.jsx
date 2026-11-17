
import { useState } from 'react'

import Navbar from '../components/Navbar'
import ScholarshipMenu from '../components/ScholarshipMenu'
import ScholarshipDetails from '../components/ScholarshipDetails'

import { scholarships } from '../data/scholarships'

export default function Home() {
  const [selectedScholarship, setSelectedScholarship] =
    useState(null)

  return (

<div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#031B4E] to-[#020617]">


      <Navbar />

      <main className="mx-auto max-w-7xl p-6">
        {!selectedScholarship ? (
          <ScholarshipMenu
            scholarships={scholarships}
            onSelect={setSelectedScholarship}
          />
        ) : (
          <ScholarshipDetails
            scholarship={selectedScholarship}
            onBack={() => setSelectedScholarship(null)}
          />
        )}
      </main>
    </div>
  )
}


