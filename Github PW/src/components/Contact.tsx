import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const Contact = () => {
  return (
    <section id="contact" className="py-20 px-6 bg-background">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Let's Connect
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-brand-secondary to-brand-accent mx-auto rounded-full mb-4" />
          <p className="text-lg text-text-subtle max-w-2xl mx-auto">
            I'm always open to discussing new opportunities, collaborations, or just having a chat about technology.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-8">
          {/* Contact Information */}
          <Card className="shadow-medium">
            <CardContent className="p-8">
              <h3 className="text-2xl font-semibold text-brand-primary mb-6">
                Get In Touch
              </h3>
              
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-secondary/10 rounded-full flex items-center justify-center">
                    <span className="text-xl">📧</span>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">Email</p>
                    <p className="text-text-subtle">henryparkin21@gmail.com</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-secondary/10 rounded-full flex items-center justify-center">
                    <span className="text-xl">💼</span>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">LinkedIn</p>
                    <p className="text-text-subtle">linkedin.com/in/henry-parkin-041953231/</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-secondary/10 rounded-full flex items-center justify-center">
                    <span className="text-xl">🐙</span>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">GitHub</p>
                    <p className="text-text-subtle">github.com/tomjedavey/CBACKTESTER</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-secondary/10 rounded-full flex items-center justify-center">
                    <span className="text-xl">📱</span>
                  </div>
                  <div>
                    <p className="font-medium text-foreground">Phone</p>
                    <p className="text-text-subtle">+44 7762319271</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
          
          {/* Call to Action */}
          <Card className="shadow-medium">
            <CardContent className="p-8 flex flex-col justify-center">
              <div className="text-center">
                <h3 className="text-2xl font-semibold text-brand-primary mb-4">
                  Ready to Work Together?
                </h3>
                
                <p className="text-text-subtle mb-8 leading-relaxed">
                  Whether you have a project in mind, want to collaborate, or just want to say hello, 
                  I'd love to hear from you. Let's create something amazing together!
                </p>
                
                <div className="space-y-4">
                  <Button 
                    className="w-full bg-gradient-to-r from-brand-secondary to-brand-accent text-white hover:from-brand-secondary/90 hover:to-brand-accent/90 transition-all duration-300 transform hover:scale-105"
                    size="lg"
                  >
                    Send Me an Email
                  </Button>
                  
                  <Button 
                    variant="outline"
                    className="w-full border-brand-secondary text-brand-secondary hover:bg-brand-secondary hover:text-white transition-all duration-300"
                    size="lg"
                  >
                    Download Resume
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-surface-muted text-center">
          <p className="text-text-subtle">
            © 2024 Henry. Built with React, TypeScript, and lots of ☕
          </p>
        </div>
      </div>
    </section>
  );
};

export default Contact;