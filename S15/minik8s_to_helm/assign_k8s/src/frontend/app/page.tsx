import SimpleFileUpload from '../components/SimpleFileUpload';

export default function Home() {
  const dogBreeds = [
    "Beagle",
    "Boxer",
    "Bulldog",
    "Dachshund",
    "German Shepherd",
    "Golden Retriever",
    "Labrador Retriever",
    "Poodle",
    "Rottweiler",
    "Yorkshire Terrier"
  ];

  return (
    <main className="container mx-auto p-4">
      <header className="text-center my-4">
        <h1 className="text-2xl font-bold">DogBreeds 🐾 Classification</h1>
        <p className="text-gray-600">powered by FastAPI, torchserve+onnx, Redis Caching, k8s, and Nextjs </p>
      </header>
      <section>
        <h2 className="text-xl font-semibold my-4">List of Dog Breeds</h2>
        <ul className="list-disc list-inside">
          {dogBreeds.map((breed) => (
            <li key={breed} className="text-gray-700">{breed}</li>
          ))}
        </ul>
      </section>
      <SimpleFileUpload />
      <footer>
        <p className="text-center  my-4">written by 🐍, hated by 😼 and ❤️ by us</p>
      </footer>
      
    </main>
  );

}
