import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const Experience = () => {
  const experiences = [
    {
      title: "GIS/Photogrammetry Technician & Visual Observer",
      company: "SummitInfrastructure",
      period: "Sept 2024 - Present",
      description: "Operated 5+ drones for LIDAR and photogrammetry projects. Conducted drone-based mapping for infrastructure projects across British Columbia, Alberta, and Toronto with expertise in track surveying and GEDO trolley operation.",
      achievements: [
        "Operated multiple drone systems for mapping projects",
        "Applied Python for GIS data analysis workflows",
        "Conducted infrastructure mapping across multiple provinces"
      ]
    },
    {
      title: "Blockchain Gaming Research",
      company: "Vempire",
      period: "Aug 2023 - Present",
      description: "Conducted research in blockchain gaming technologies under NDA. Analyzed emerging trends and technologies in the intersection of gaming and blockchain.",
      achievements: [
        "Research on blockchain gaming innovations",
        "Analysis of emerging gaming technologies",
        "Strategic insights for gaming industry applications"
      ]
    },
    {
      title: "Investment Banking Insight Placement",
      company: "Royal Bank of Canada",
      period: "June 2023 - Sept 2023",
      description: "Shadowed the Head of Equity Capital Markets and attended client meetings with major institutions like Fidelity. Gained exposure to ECM, DCM, FX, Fixed Income, and Commodities teams.",
      achievements: [
        "Attended high-level client meetings with institutions",
        "Observed multiple trading and capital markets teams",
        "Gained comprehensive investment banking experience"
      ]
    },
    {
      title: "Financial Insight Intern",
      company: "Savills Private Finance",
      period: "July 2023 - Aug 2023",
      description: "Gained exposure to mortgage and insurance products while exploring rate modeling and debt structuring alongside senior directors.",
      achievements: [
        "Explored mortgage and insurance product structures",
        "Learned rate modeling techniques",
        "Worked directly with senior leadership team"
      ]
    },
    {
      title: "Marketing & Sales Development",
      company: "Plura Innovations",
      period: "Mar 2023 - Dec 2023",
      description: "Revamped marketing outreach strategies for composite bridge systems, directly contributing to significant business growth and client acquisition.",
      achievements: [
        "Revamped marketing outreach strategies",
        "Directly contributed to securing £1.5M order",
        "Improved sales development processes"
      ]
    }
  ];

  return (
    <section id="experience" className="py-20 px-6 bg-surface">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Work Experience
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-brand-secondary to-brand-accent mx-auto rounded-full" />
        </div>
        
        <div className="relative">
          {/* Timeline Line */}
          <div className="hidden md:block absolute left-1/2 transform -translate-x-px h-full w-0.5 bg-gradient-to-b from-brand-secondary to-brand-accent" />
          
          <div className="space-y-12">
            {experiences.map((exp, index) => (
              <div key={index} className={`relative flex items-center ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                {/* Timeline Dot */}
                <div className="hidden md:block absolute left-1/2 transform -translate-x-1/2 w-4 h-4 bg-brand-accent rounded-full border-4 border-white shadow-lg z-10" />
                
                {/* Content Card */}
                <div className={`w-full md:w-5/12 ${index % 2 === 0 ? 'md:pr-8' : 'md:pl-8'}`}>
                  <Card className="shadow-medium hover:shadow-strong transition-all duration-300 transform hover:-translate-y-1">
                    <CardHeader>
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-2">
                        <CardTitle className="text-xl font-bold text-brand-primary">
                          {exp.title}
                        </CardTitle>
                        <span className="text-sm text-text-subtle font-medium">
                          {exp.period}
                        </span>
                      </div>
                      <CardDescription className="text-brand-secondary font-semibold">
                        {exp.company}
                      </CardDescription>
                    </CardHeader>
                    
                    <CardContent>
                      <p className="text-text-subtle mb-4 leading-relaxed">
                        {exp.description}
                      </p>
                      
                      <div className="space-y-2">
                        <h4 className="font-semibold text-foreground text-sm">Key Achievements:</h4>
                        <ul className="space-y-1">
                          {exp.achievements.map((achievement, i) => (
                            <li key={i} className="flex items-center text-sm text-text-subtle">
                              <div className="w-1.5 h-1.5 bg-brand-accent rounded-full mr-3 flex-shrink-0" />
                              {achievement}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Experience;