import React, { useState } from 'react';
import { MapPin, Briefcase, IndianRupee, ArrowRight, ShieldCheck, Zap, Maximize, Map } from 'lucide-react';

export default function LandingPage({ onGenerate }) {
  const [industryType, setIndustryType] = useState('Pharmaceutical Manufacturing');
  const [district, setDistrict] = useState('Pune');
  const [investmentScale, setInvestmentScale] = useState(50);
  const [unitSize, setUnitSize] = useState('large');
  const [existingLand, setExistingLand] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onGenerate({ 
      industry_type: industryType, 
      district: district, 
      investment_scale_crores: parseFloat(investmentScale),
      unit_size: unitSize,
      existing_land: existingLand
    });
  };

  return (
    <div className="w-full h-full overflow-y-auto flex flex-col md:flex-row bg-[#F7F4EC] text-[#1C2333] font-['Inter']">
      {/* Left side - Branding / Context */}
      <div className="hidden md:flex flex-1 p-12 flex-col justify-between relative overflow-hidden border-r border-[#1C2333]">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, #1C2333 1px, transparent 0)', backgroundSize: '32px 32px' }}></div>
        
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 border border-[#1C2333] flex items-center justify-center font-['Fraunces']">
              <span className="font-bold text-2xl">N</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight font-['Fraunces'] uppercase">Nyapath</h1>
          </div>
          
          <h2 className="text-5xl font-['Fraunces'] leading-tight mb-6">
            Maharashtra's Industrial<br/>Compliance GPS.
          </h2>
          <p className="text-[#3A5A78] text-lg max-w-md leading-relaxed">
            Stop building generic portals. We map your entire regulatory journey, predict bottlenecks, and audit your documents before you file a single application.
          </p>
        </div>

        <div className="relative z-10 grid grid-cols-2 gap-6 mt-12">
          <div className="p-4 border border-[#1C2333]">
            <ShieldCheck className="w-8 h-8 text-[#5C7A5E] mb-2" />
            <div className="font-bold font-['IBM_Plex_Mono'] text-sm uppercase">EoDB Aligned</div>
            <div className="text-sm text-[#3A5A78]">Built for MAITRI 2026</div>
          </div>
          <div className="p-4 border border-[#1C2333]">
            <Zap className="w-8 h-8 text-[#C6742B] mb-2" />
            <div className="font-bold font-['IBM_Plex_Mono'] text-sm uppercase">Llama-3 Powered</div>
            <div className="text-sm text-[#3A5A78]">Instant RAG intelligence</div>
          </div>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-[#F7F4EC] relative">
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'linear-gradient(#1C2333 1px, transparent 1px), linear-gradient(90deg, #1C2333 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
        <div className="w-full max-w-md relative z-10">
          <div className="mb-10 md:hidden">
            <h1 className="text-3xl font-['Fraunces'] text-[#1C2333] mb-2">Nyapath</h1>
            <p className="text-[#3A5A78]">Maharashtra's Industrial Compliance GPS</p>
          </div>

          <h2 className="text-3xl font-['Fraunces'] text-[#1C2333] mb-3">Plan your journey</h2>
          <p className="text-[#3A5A78] mb-8 font-medium">Enter your project profile to generate a customized regulatory roadmap.</p>
          
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="group">
              <label className="block text-xs font-['IBM_Plex_Mono'] font-bold uppercase tracking-wide text-[#3A5A78] mb-2 border-b border-[#1C2333] pb-1">Industry Sector</label>
              <div className="relative mt-2">
                <Briefcase className="absolute left-4 top-3.5 text-[#3A5A78] w-5 h-5 transition-colors" />
                <input 
                  type="text" 
                  value={industryType}
                  onChange={(e) => setIndustryType(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-transparent border border-[#1C2333] focus:ring-1 focus:ring-[#1C2333] outline-none transition-all font-medium text-[#1C2333] rounded-none" 
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="group">
                <label className="block text-xs font-['IBM_Plex_Mono'] font-bold uppercase tracking-wide text-[#3A5A78] mb-2 border-b border-[#1C2333] pb-1">District</label>
                <div className="relative mt-2">
                  <MapPin className="absolute left-3 top-3 text-[#3A5A78] w-5 h-5 transition-colors" />
                  <select 
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-transparent border border-[#1C2333] focus:ring-1 focus:ring-[#1C2333] outline-none transition-all font-medium text-[#1C2333] rounded-none appearance-none" 
                    required
                  >
                    <option value="Pune">Pune</option>
                    <option value="Mumbai">Mumbai</option>
                    <option value="Nagpur">Nagpur</option>
                    <option value="Nashik">Nashik</option>
                    <option value="Aurangabad">Aurangabad</option>
                  </select>
                </div>
              </div>

              <div className="group">
                <label className="block text-xs font-['IBM_Plex_Mono'] font-bold uppercase tracking-wide text-[#3A5A78] mb-2 border-b border-[#1C2333] pb-1">Investment (Cr)</label>
                <div className="relative mt-2">
                  <IndianRupee className="absolute left-3 top-3 text-[#3A5A78] w-5 h-5 transition-colors" />
                  <input 
                    type="number" 
                    min="1"
                    value={investmentScale}
                    onChange={(e) => setInvestmentScale(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-transparent border border-[#1C2333] focus:ring-1 focus:ring-[#1C2333] outline-none transition-all font-medium text-[#1C2333] rounded-none" 
                    required
                  />
                </div>
              </div>
            </div>

            <div className="group pt-2">
              <label className="block text-xs font-['IBM_Plex_Mono'] font-bold uppercase tracking-wide text-[#3A5A78] mb-3 border-b border-[#1C2333] pb-1">Unit Size</label>
              <div className="flex gap-4">
                {['small', 'medium', 'large'].map((size) => (
                  <label key={size} className="flex-1 flex items-center cursor-pointer border border-[#1C2333] p-2 hover:bg-[#1C2333]/5">
                    <input 
                      type="radio" 
                      name="unitSize" 
                      value={size}
                      checked={unitSize === size}
                      onChange={(e) => setUnitSize(e.target.value)}
                      className="hidden" 
                    />
                    <div className={`w-3 h-3 border border-[#1C2333] mr-2 flex items-center justify-center ${unitSize === size ? 'bg-[#C6742B]' : 'bg-transparent'}`}>
                    </div>
                    <span className="text-sm font-['IBM_Plex_Mono'] uppercase">{size}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="group pt-2">
              <label className="flex items-center cursor-pointer border border-[#1C2333] p-4 hover:bg-[#1C2333]/5">
                <input 
                  type="checkbox" 
                  checked={existingLand}
                  onChange={(e) => setExistingLand(e.target.checked)}
                  className="hidden" 
                />
                <div className={`w-5 h-5 border border-[#1C2333] mr-3 flex items-center justify-center ${existingLand ? 'bg-[#1C2333]' : 'bg-transparent'}`}>
                  {existingLand && <div className="w-3 h-3 bg-[#C6742B]" />}
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-['Fraunces'] font-bold uppercase tracking-wider text-[#1C2333]">Existing Land / Premises</span>
                  <span className="text-[10px] font-['IBM_Plex_Mono'] text-[#3A5A78] uppercase mt-1">Skip land acquisition processes</span>
                </div>
              </label>
            </div>

            <button 
              type="submit"
              className="w-full mt-6 bg-[#1C2333] text-[#F7F4EC] font-['IBM_Plex_Mono'] font-bold py-4 flex items-center justify-center gap-2 transition-transform active:scale-[0.98] rounded-none uppercase tracking-widest text-sm"
            >
              Generate Intelligence Report
              <ArrowRight className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
