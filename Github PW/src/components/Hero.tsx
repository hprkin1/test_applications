import { Button } from "@/components/ui/button";
import heroBackground from "@/assets/hero-background.jpg";

const Hero = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    element?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${heroBackground})` }}
      />
      
      {/* Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-brand-primary/90 via-brand-secondary/80 to-brand-accent/70" />
      
      {/* Content */}
      <div className="relative z-10 text-center text-white px-6 max-w-4xl">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-fade-in">
          Hi, I'm <span className="bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent">Henry</span>
        </h1>
        
        <p className="text-xl md:text-2xl mb-4 opacity-90 animate-fade-in-delay-1">
          Motivated & Analytically Driven Individual
        </p>
        
        <p className="text-lg md:text-xl mb-8 opacity-80 max-w-2xl mx-auto animate-fade-in-delay-2">
          Passionate about creating digital experiences that make a difference. 
          I turn ideas into elegant, functional solutions.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-delay-3">
          <Button 
            variant="hero"
            size="lg"
            onClick={() => scrollToSection("about")}
            className="text-lg px-8 py-3"
          >
            Learn More About Me
          </Button>
          
          <Button 
            variant="hero-outline"
            size="lg"
            onClick={() => scrollToSection("contact")}
            className="text-lg px-8 py-3"
          >
            Get In Touch
          </Button>
        </div>
      </div>
      
      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  );
};

export default Hero;