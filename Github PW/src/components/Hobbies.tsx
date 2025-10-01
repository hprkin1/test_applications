import { Card, CardContent } from "@/components/ui/card";

const Hobbies = () => {
  const hobbies = [
    {
      title: "Rugby Union",
      description: "Yorkshire Rugby Academy winger U17's. The discipline and teamwork from rugby shapes my approach to collaboration.",
      icon: "🏉"
    },
    {
      title: "Rugby League",
      description: "Represented England Rugby League U17's against France. International competition taught me resilience under pressure.",
      icon: "🏴󠁧󠁢󠁥󠁮󠁧󠁿"
    },
    {
      title: "Sprinting",
      description: "Achieved U16 English qualifying time for 100m sprint (11.02s) in 2022. Speed and precision drive excellence.",
      icon: "🏃‍♂️"
    },
    {
      title: "Philosophy & Stoicism",
      description: "Studying Marcus Aurelius' 'Meditations' and Aristotle's 'Ethics'. Ancient wisdom guides modern decision-making.",
      icon: "📚"
    },
    {
      title: "Chess",
      description: "Intermediate level strategic thinking. Chess develops the analytical mindset I apply to complex problems.",
      icon: "♟️"
    },
    {
      title: "Skiing",
      description: "Former member of the British Ski Academy in 2017. High-speed decision making and risk assessment on the slopes.",
      icon: "⛷️"
    }
  ];

  return (
    <section id="hobbies" className="py-20 px-6 bg-surface">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">
            Beyond Finance & Code
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-brand-secondary to-brand-accent mx-auto rounded-full mb-4" />
          <p className="text-lg text-text-subtle max-w-2xl mx-auto">
            When I'm not analyzing data or markets, I'm pursuing athletics and philosophy that develop my character and strategic thinking.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {hobbies.map((hobby, index) => (
            <Card 
              key={index} 
              className="group hover:shadow-medium transition-all duration-300 transform hover:-translate-y-2 cursor-pointer border-0 shadow-soft"
            >
              <CardContent className="p-6 text-center">
                <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
                  {hobby.icon}
                </div>
                
                <h3 className="text-xl font-semibold text-brand-primary mb-3">
                  {hobby.title}
                </h3>
                
                <p className="text-text-subtle leading-relaxed">
                  {hobby.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="mt-16 text-center">
          <div className="bg-background p-8 rounded-2xl shadow-soft max-w-3xl mx-auto">
            <h3 className="text-2xl font-semibold text-brand-primary mb-4">
              Life Philosophy
            </h3>
            <p className="text-lg text-text-subtle leading-relaxed">
              Athletic excellence and philosophical study have shaped my approach to professional challenges. The discipline 
              from competitive rugby, the precision from sprinting, and the wisdom from Stoic philosophy all contribute to my 
              analytical mindset. Whether it's the strategic thinking from chess or the risk assessment from skiing, each pursuit 
              enhances my ability to perform under pressure and make thoughtful decisions.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hobbies;