import { Link } from "@solidjs/router";

type HeaderProps = {
  assetId: string;
  handleClickAssetSelector: (e: MouseEvent) => void;
};

export default function Header(props: HeaderProps) {
  return (
    <header class="flex gap-2 justify-between text-xl p-2 shadow-lg sticky top-0 bg-slate-200">
      <h1 class="flex gap-2 items-center">
        Showing: <b>{props.assetId}</b>
      </h1>
      {/* <div class="flex gap-2 items-center"> */}
      {/* <Link ref={""}/> */}
      {/* <p>show plots(dummy link)</p> */}
      {/* </div> */}
      <div class="flex gap-2 justify-center font-bold">
        <button
          class="rounded-md shadow-md bg-slate-600 text-white p-2"
          onClick={props.handleClickAssetSelector}
        >
          EdanMeyerVpt
        </button>
        <button
          class="rounded-md shadow-md bg-slate-600 text-white p-2"
          onClick={props.handleClickAssetSelector}
        >
          IEEEVR2022Ogawa
        </button>
      </div>
    </header>
  );
}
