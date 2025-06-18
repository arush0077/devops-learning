const Skeleton = () => {
  return (
    <div className="w-full">
      <div className="w-full mb-4 text-center">
        <div className="w-full h-28 skeleton"></div>
      </div>

      <div className="w-full flex items-center gap-4 mb-8">
        <div className="w-full h-96 skeleton"></div>
      </div>

      <div className="w-full h-20 skeleton"></div>
    </div>
  );
};

export default Skeleton;
