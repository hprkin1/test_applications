const About = () => {
  return (
    <section id="about" className="py-20 px-6 bg-background">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            About Me
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-brand-secondary to-brand-accent mx-auto rounded-full" />
        </div>
        
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h3 className="text-2xl md:text-3xl font-semibold text-brand-primary">
              My Journey
            </h3>
            
            <p className="text-lg text-text-subtle leading-relaxed">
              My journey into technology began with curiosity and evolved into a passion for creating 
              meaningful digital experiences. I believe in the power of code to solve real-world problems 
              and improve people's lives.
            </p>
            
            <p className="text-lg text-text-subtle leading-relaxed">
              Over the years, I've had the privilege of working on diverse projects that challenged me 
              to grow as both a developer and a problem solver. Each experience has shaped my approach 
              to building software that is not just functional, but delightful to use.
            </p>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-brand-accent rounded-full" />
                <span className="text-foreground font-medium">
                  Passionate about clean, maintainable code
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-brand-accent rounded-full" />
                <span className="text-foreground font-medium">
                  Always learning and staying current with technology
                </span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-brand-accent rounded-full" />
                <span className="text-foreground font-medium">
                  Believer in collaborative development and knowledge sharing
                </span>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="bg-surface p-8 rounded-2xl shadow-medium">
              <h4 className="text-xl font-semibold text-brand-primary mb-4">
                What Drives Me
              </h4>
              
              <blockquote className="text-text-subtle italic text-lg leading-relaxed">
                "The best way to predict the future is to create it. I'm passionate about 
                building solutions that make tomorrow better than today."
              </blockquote>
              
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="flex items-center justify-between text-sm text-text-subtle">
                  <span>Years of Experience</span>
                  <span className="font-semibold text-brand-primary">5+</span>
                </div>
                
                <div className="flex items-center justify-between text-sm text-text-subtle mt-2">
                  <span>Projects Completed</span>
                  <span className="font-semibold text-brand-primary">50+</span>
                </div>
                
                <div className="flex items-center justify-between text-sm text-text-subtle mt-2">
                  <span>Coffee Consumed</span>
                  <span className="font-semibold text-brand-primary">∞</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;