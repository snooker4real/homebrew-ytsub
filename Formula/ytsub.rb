class Ytsub < Formula
  include Language::Python::Virtualenv

  desc "Affiche ou telecharge la transcription (sous-titres) d'une video YouTube"
  homepage "https://github.com/snooker4real/homebrew-ytsub"
  url "https://github.com/snooker4real/homebrew-ytsub/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REMPLACER_PAR_LE_SHA256_DU_TARBALL"
  license "MIT"

  depends_on "python@3.13"

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/fd/11/b524cbd9bbdaca58608e4cf4053fd463417549e1959fa8d3aa18319f9555/certifi-2026.10.23.tar.gz"
    sha256 "a9895e6e2758b371e0545e321a3a8fd1fcfd9829ada8824a936dfb16aaaf36cd"
  end

  resource "charset-normalizer" do
    url "https://files.pythonhosted.org/packages/33/1c/f41d4e74c28ab327ff3acd36053f7ea506c55872d7a90b0fa71aa3ab0c89/charset_normalizer-3.5.2.tar.gz"
    sha256 "39de2a259fc954455c57274dc94c79d5842774e1247a016aff30bc0efed0f4ef"
  end

  resource "defusedxml" do
    url "https://files.pythonhosted.org/packages/0f/d5/c66da9b79e5bdb124974bfe172b4daf3c984ebd9c2a06e2b8a4dc7331c72/defusedxml-0.7.1.tar.gz"
    sha256 "1bb3032db185915b62d7c6209c5a8792be6a32ab2fedacc84e01b52c51aa3e69"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/f5/08/8eea9d4b8302028f3abb2c0813953f7aec26d33b7a8960ed760e65ff29fa/idna-3.20.tar.gz"
    sha256 "a7db850025b95ded1eae8a46181a1a6c56c92c96f0e2b005d9ff8dc0210cab44"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/ac/c3/e2a2b89f2d3e2179abd6d00ebd70bff6273f37fb3e0cc209f48b39d00cbf/requests-2.34.2.tar.gz"
    sha256 "f288924cae4e29463698d6d60bc6a4da69c89185ad1e0bcc4104f584e960b9ed"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/e3/05/b17359e1cefb4f909b5e40b1b90a496d987258916dbbf88e842c729f510e/urllib3-2.8.0.tar.gz"
    sha256 "63bf2ead4c879426ebf22ef2a781eeb4aa3b4ae798a0435506f8687fd5bb9b63"
  end

  resource "youtube-transcript-api" do
    url "https://files.pythonhosted.org/packages/60/43/4104185a2eaa839daa693b30e15c37e7e58795e8e09ec414f22b3db54bec/youtube_transcript_api-1.2.4.tar.gz"
    sha256 "b72d0e96a335df599d67cee51d49e143cff4f45b84bcafc202ff51291603ddcd"
  end

  resource "yt-dlp" do
    url "https://files.pythonhosted.org/packages/83/31/4be3987022a6244550ab6a3afe45ad10ac10b5e5ab8874bd8eecc7f8b937/yt_dlp-2026.10.26.tar.gz"
    sha256 "abe5c6b94c3b2f0560500add1c42e0a97641752743a5b65588ac2007a6e23eb6"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "ytsub #{version}", shell_output("#{bin}/ytsub --version")
    assert_match "usage", shell_output("#{bin}/ytsub 2>&1", 2)
  end
end
