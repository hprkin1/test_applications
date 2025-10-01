import { Badge } from "@/components/ui/badge";

const Skills = () => {
  const skillCategories = [
    {
      title: "Programming & Analysis",
      skills: ["Python", "Data Analysis", "Machine Learning", "Algorithmic Trading", "Backtesting", "TypeScript", "React", "JavaScript"]
    },
    {
      title: "Finance & Trading",
      skills: ["FX Analysis", "Crypto Analysis", "Algorithmic Trading", "Market Research", "Risk Assessment", "Portfolio Analysis"]
    },
    {
      title: "GIS & Technical Tools",
      skills: ["GIS Software", "Photogrammetry", "LIDAR Operations", "Drone Technology", "GEDO Trolley", "Track Surveying", "Mapping Workflows"]
    },
    {
      title: "Sales & Business",
      skills: ["Sales Outreach", "Cold Emailing", "Cold Calling", "Client Relations", "Market Analysis", "Lead Generation"]
    },
    {
      title: "Certifications & Licenses",
      skills: ["Advanced Python Proficiency", "RPAS License", "AST 1 Avalanche Safety", "Proserve License", "Erail-Safe Authentication"]
    }
  ];

  const proficiencyLevels = [
    { skill: "Python & Data Analysis", level: 90 },
    { skill: "GIS & Photogrammetry", level: 85 },
    { skill: "Financial Analysis", level: 80 },
    { skill: "Sales & Outreach", level: 85 },
    { skill: "Drone Operations", level: 90 },
    { skill: "Market Research", level: 75 }
  ];

  return (
    <section id="skills" className="py-20 px-6 bg-background">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Skills & Expertise
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-brand-secondary to-brand-accent mx-auto rounded-full" />
        </div>
        
        <div className="grid lg:grid-cols-2 gap-12">
          {/* Skills by Category */}
          <div>
            <h3 className="text-2xl font-semibold text-brand-primary mb-8">
              Technologies
            </h3>
            
            <div className="space-y-8">
              {skillCategories.map((category, index) => (
                <div key={index}>
                  <h4 className="text-lg font-semibold text-foreground mb-4">
                    {category.title}
                  </h4>
                  
                  <div className="flex flex-wrap gap-2">
                    {category.skills.map((skill, skillIndex) => (
                      <Badge 
                        key={skillIndex} 
                        variant="secondary"
                        className="px-3 py-1 text-sm hover:bg-brand-secondary hover:text-white transition-colors duration-200"
                      >
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Proficiency Levels */}
          <div>
            <h3 className="text-2xl font-semibold text-brand-primary mb-8">
              Proficiency Levels
            </h3>
            
            <div className="space-y-6">
              {proficiencyLevels.map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-foreground font-medium">
                      {item.skill}
                    </span>
                    <span className="text-text-subtle text-sm">
                      {item.level}%
                    </span>
                  </div>
                  
                  <div className="w-full bg-surface-muted rounded-full h-2.5">
                    <div 
                      className="bg-gradient-to-r from-brand-secondary to-brand-accent h-2.5 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${item.level}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-8 p-6 bg-surface rounded-xl shadow-soft">
              <h4 className="font-semibold text-brand-primary mb-3">
                Always Learning
              </h4>
              <p className="text-text-subtle leading-relaxed">
                Technology evolves rapidly, and I'm committed to continuous learning. 
                Currently exploring AI/ML integration in web applications and advanced 
                cloud architecture patterns.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Skills;