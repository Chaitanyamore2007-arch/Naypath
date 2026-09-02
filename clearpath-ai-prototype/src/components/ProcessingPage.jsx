import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export default function ProcessingPage({ projectData }) {
  const [step, setStep] = useState(0);
  const steps = [
    "Querying Maharashtra Regulatory Graph...",
    "Analyzing Factories Act provisions...",
    "Matching PCB consent conditions...",
    "Structuring compliance sequence..."
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setStep(s => (s + 1) % steps.length);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center bg-[#F7F4EC] relative">
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'linear-gradient(#1C2333 1px, transparent 1px), linear-gradient(90deg, #1C2333 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
      <div className="relative w-32 h-32 mb-8 z-10">
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
          className="absolute inset-0 border border-[#1C2333] rounded-full"
          style={{ borderStyle: 'dashed' }}
        />
        <motion.div 
          animate={{ rotate: -360 }}
          transition={{ repeat: Infinity, duration: 4, ease: "linear" }}
          className="absolute inset-4 border border-[#3A5A78] rounded-full flex items-center justify-center"
        >
          <div className="w-1 h-8 bg-[#C6742B] absolute top-0 -translate-y-1/2"></div>
          <div className="w-1 h-8 bg-[#3A5A78] absolute bottom-0 translate-y-1/2"></div>
        </motion.div>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xl font-bold text-[#1C2333] font-['Fraunces']">N</span>
        </div>
      </div>
      <h2 className="text-3xl font-bold text-[#1C2333] mb-4 font-['Fraunces'] z-10">Calculating Route</h2>
      {projectData && (
        <p className="text-[#1C2333] font-['Fraunces'] mb-3 z-10 text-center max-w-md">
          {projectData.industry_type} · {projectData.district} · ₹{projectData.investment_scale_crores} Cr
        </p>
      )}
      <p className="text-[#3A5A78] font-['IBM_Plex_Mono'] text-sm uppercase tracking-widest z-10">{steps[step]}</p>
    </div>
  );
}
